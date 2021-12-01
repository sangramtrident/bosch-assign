from django.shortcuts import render
from .serializers import *
from calendar import timegm
from datetime import datetime
import logging
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework_jwt.settings import api_settings
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.models import User


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

logger = logging.getLogger(__name__)


def jwt_payload_handler(user):
    payload = {
        'user_id': user.id,
        'username': user.email,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    return payload


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializers(user, context={'request': request}).data
    }


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                user = User(**serializer.data)
                if user.id > 0:
                    group = Group.objects.filter(name__exact='Users').first()
                    user_db = User.objects.get(id=user.id)
                    user_db.groups.add(group)
                    user_db.save()
                    return_data = UserSerializers(user).data
                    jwt_token = jwt_encode_handler(jwt_payload_handler(user))
                    response = Response(return_data, status=status.HTTP_201_CREATED)
                    response['X-AUTH-TOKEN'] = jwt_token
                    return response
            errors = dict()
            for key in serializer.errors:
                errors.__setitem__(key, serializer.errors[key][0].capitalize())
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e.__cause__)
            logger.error(e)
            return Response({"message": e.__cause__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.instance
                request.user = user
                user.last_login = timezone.now()
                user.save()
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user_ser = UserSerializers(user, many=False)
                ret_data = user_ser.data
                resp = Response(ret_data)
                resp['X-AUTH-TOKEN'] = token
                return resp
            errors = dict()
            for key in serializer.errors:
                errors.__setitem__(key, serializer.errors[key][0].capitalize())
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e.__cause__)
            logger.error(e)
            return Response({"message": e.__cause__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

