from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    # Query Module:
    # """post query             : api/queries/post/""",
    # """Method: POST, BODY: {KEY: 'subject', 'file', 'description', }""",
    
    url(r'^post/$', QueryCreateView.as_view(), name="post-query"),

    # """Login             : api/response-to-queries/""",
    # """Method: POST, BODY: {KEY: 'query', 'response'}""",
    url(r'^response-to-queries/$', ResponseToQueryView.as_view(), name="response-to-query"),


]