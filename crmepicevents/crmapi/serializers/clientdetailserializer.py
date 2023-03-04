"""
serializer class for Client model
return the entire details of a Client
    @get_sales_contact : included sales contact details
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from ...authentication.serializers.userlistserializer import UserListSerializer
from .contractlistserializer import ContractListSerializer
from ..models.client import Client


class ClientDetailSerializer(ModelSerializer):
    id = serializers.ReadOnlyField()

    sales_contact = SerializerMethodField()
    contracts = SerializerMethodField()

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
            'sales_contact',
            'contracts'
        ]

    def get_sales_contact(self, instance):
        queryset = instance.sales_contact.all()
        serializer = UserListSerializer(queryset, many=True)
        return serializer.data

    def get_contracts(self, instance):
        queryset = instance.contracts.all()
        serializer = ContractListSerializer(queryset, many=True)
        return serializer.data
