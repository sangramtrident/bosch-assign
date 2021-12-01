from rest_framework import serializers
from .models import *



class QuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Query
        fields = '__all__'


class ResponseToQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseToQuery
        fields = '__all__'
