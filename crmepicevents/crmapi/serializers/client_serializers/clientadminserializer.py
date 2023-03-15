from rest_framework import serializers

from .clientbaseserializer import ClientBaseSerializer
from crmapi.models.client import Client


class ClientAdminSerializer(ClientBaseSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Client
        fields = (
            'id',
            'sales_contact',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
            'date_created',
            'date_updated',
            'contracts'
        )
