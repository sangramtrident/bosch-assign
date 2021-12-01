from rest_framework import serializers
from account.models import User
from account.error_msg import UserSerErrMsg
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=20, min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['name'],
                                                 validated_data['phone'],
                                                 validated_data['email'],
                                                 validated_data['password'],
                                                 )
        return user

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'email', 'password']
        extra_kwargs = {
            "name": {"error_messages": UserSerErrMsg.name},
            "phone": {"error_messages": UserSerErrMsg.phone},
            "email": {"error_messages": UserSerErrMsg.email},
            "password": {'write_only': True, "error_messages": UserSerErrMsg.password},
        }
        read_only_fields = ('id', 'is_admin')

class UserSerializers(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['name'],
                                                 validated_data['phone'],
                                                 validated_data['email'],
                                                 validated_data['password'],
                                                 )
        return user

    class Meta:
        model = User
        fields = (
            'id', 'name', 'phone', 'email', 'gender', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=True, error_messages={'required': 'Username required'})
    password = serializers.CharField(max_length=255, required=True, error_messages={"required": "Password required"})

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs, ):
        user = authenticate(
            email=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Invalid phone or password')
        self.instance = user
        return user