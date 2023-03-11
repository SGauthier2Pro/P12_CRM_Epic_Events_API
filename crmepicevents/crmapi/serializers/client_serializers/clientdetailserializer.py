"""
serializer class for Client model
return the entire details of a Client
    @get_sales_contact : included sales contact details
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers
from django.contrib.auth.models import User

from .clientbaseserializer import ClientBaseSerializer
from authentication.serializers.userlistserializer import UserListSerializer
from crmapi.serializers.contract_serializers.contractlistserializer import ContractListSerializer
from crmapi.models.client import Client
from crmapi.models.contract import Contract


class ClientDetailSerializer(ClientBaseSerializer):
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
        if instance.sales_contact:

            queryset = User.objects.filter(pk=instance.sales_contact.id)
            serializer = UserListSerializer(queryset, many=True)
            return serializer.data

    def get_contracts(self, instance):
        if instance.contracts:
            queryset = instance.contracts.all()
            serializer = ContractListSerializer(queryset, many=True)
            return serializer.data
