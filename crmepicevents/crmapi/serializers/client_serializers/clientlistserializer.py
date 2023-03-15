"""
serializer class for Client model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework import serializers

from .clientbaseserializer import ClientBaseSerializer

from crmapi.models.client import Client


class ClientListSerializer(ClientBaseSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
        ]
