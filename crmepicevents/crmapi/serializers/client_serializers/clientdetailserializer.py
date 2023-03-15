"""
serializer class for Client model
return the entire details of a Client
    @get_sales_contact : included sales contact details
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework import serializers

from .clientbaseserializer import ClientBaseSerializer
from crmapi.models.client import Client


class ClientDetailSerializer(ClientBaseSerializer):
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
            'date_created',
            'date_updated',
            'confirmed',
            'sales_contact',
            'contracts'
        ]

