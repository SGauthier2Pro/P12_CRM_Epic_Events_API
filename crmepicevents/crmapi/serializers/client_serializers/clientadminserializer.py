from rest_framework import serializers

from .clientbaseserializer import ClientBaseSerializer
from crmapi.serializers.contract_serializers.contractlistserializer import \
    ContractListSerializer
from authentication.serializers.userlistserializer import UserListSerializer
from crmapi.models.client import Client


class CustomerAdminSerializer(ClientBaseSerializer):
    id = serializers.ReadOnlyField()

    sales_contact = serializers.SerializerMethodField()
    contracts = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = (
            'id',
            'readable_sales_contact',
            'sales_contact',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'mobile_number',
            'company_name',
            'date_created',
            'date_updated',
            'group',
            'events',
            'contracts'
        )

    def get_sales_contact(self, instance):
        queryset = instance.sales_contact.all()
        serializer = UserListSerializer(queryset, many=True)
        return serializer.data

    def get_contracts(self, instance):
        queryset = instance.contracts.all()
        serializer = ContractListSerializer(queryset, many=True)
        return serializer.data
