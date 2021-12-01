from django.conf.urls import url
from django.urls import path
from django.contrib.auth.models import Group
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from swagger.swagger_views import schema_view
from .views import *


urlpatterns = [
    # Django REST Framework JWT Authentication
    url(r'^users/api-token-auth/', obtain_jwt_token),
    url(r'^users/api-token-refresh/', refresh_jwt_token),
    url(r'^users/api-token-verify/', verify_jwt_token),

    # Swagger docs api
    url(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # User Module:
    # """register user             : api/users/register/""",
    # """Method: POST, BODY: {KEY: 'name', 'email', 'phone', 'password'}""",
    # url(r'^users/register/$', UserCreateView.as_view(), name="user-create"),
    url(r'^users/register/$', UserRegisterAPIView.as_view(), name="user-create"),

    # """Login             : api/users/api-login/""",
    # """Method: POST, BODY: {KEY: username, password}""",
    url(r'^users/login/$', UserLoginAPIView.as_view(), name="user-login"),

    ]

def create_default_user_group():
    group_names = ["Users", "Mentors"]
    try:
        for name in group_names:
            if not Group.objects.filter(name__exact=name).exists():
                group = Group(name=name)
                group.save()
    except:
        pass


create_default_user_group()
