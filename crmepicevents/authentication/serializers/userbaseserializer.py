"""
serializer base class for User model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework import serializers

from crmapi.models.client import Client
from crmapi.serializers.client_serializers.clientlistserializer import \
    ClientListSerializer

from crmapi.models.contract import Contract
from crmapi.serializers.contract_serializers.contractlistserializer import \
    ContractListSerializer

from crmapi.models.event import Event
from crmapi.serializers.event_serializers.eventlistserializer import \
    EventListSerializer


class UserBaseSerializer(serializers.ModelSerializer):
    # readonly fields
    id = serializers.ReadOnlyField()

    # data formatting
    date_joined = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    last_login = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S",
        read_only=True
    )
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    # misc user data's
    assigned_customers = serializers.SerializerMethodField()
    assigned_contracts = serializers.SerializerMethodField()
    assigned_events = serializers.SerializerMethodField()

    def get_assigned_customers(self, instance):
        queryset = Client.objects.filter(sales_contact=instance)
        serializer = ClientListSerializer(queryset, many=True)
        return serializer.data

    def get_assigned_contracts(self, instance):
        queryset = Contract.objects.filter(client__sales_contact=instance)
        serializer = ContractListSerializer(queryset, many=True)
        return serializer.data

    def get_assigned_events(self, instance):
        queryset = Event.objects.filter(support_contact=instance)
        serializer = EventListSerializer(queryset, many=True)
        return serializer.data
