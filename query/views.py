import datetime

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
import logging


logger = logging.getLogger(__name__)

@permission_classes((IsAuthenticated,))
class QueryCreateView(generics.CreateAPIView):
    serializer_class = QuerySerializer

    def post(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.id
            serializer = QuerySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=request.user.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            errors = dict()
            for key in serializer.errors:
                if type(serializer.errors[key]) is dict:
                    for inner_key in serializer.errors[key]:
                        errors.__setitem__(key + "." + inner_key, serializer.errors[key][inner_key][0].capitalize())
                else:
                    errors.__setitem__(key, serializer.errors[key][0].capitalize())
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e.__cause__)
            logger.error(e)
            return Response({"message": e.__cause__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((IsAuthenticated,))
class ResponseToQueryView(generics.CreateAPIView):
    serializer_class = ResponseToQuerySerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = ResponseToQuerySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            errors = dict()
            for key in serializer.errors:
                if type(serializer.errors[key]) is dict:
                    for inner_key in serializer.errors[key]:
                        errors.__setitem__(key + "." + inner_key, serializer.errors[key][inner_key][0].capitalize())
                else:
                    errors.__setitem__(key, serializer.errors[key][0].capitalize())
            return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e.__cause__)
            logger.error(e)
            return Response({"message": e.__cause__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)