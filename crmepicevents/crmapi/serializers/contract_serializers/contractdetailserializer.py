"""
serializer details class for Contract model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers

from .contractbaseserializer import ContractBaseSerializer
from crmapi.serializers.event_serializers.eventlistserializer import EventListSerializer
from crmapi.serializers.client_serializers.clientlistserializer import \
    ClientListSerializer

from crmapi.models.contract import Contract
from crmapi.models.client import Client
from crmapi.models.event import Event


class ContractDetailSerializer(ContractBaseSerializer):
    id = serializers.ReadOnlyField()
    event = SerializerMethodField()
    client = SerializerMethodField()

    class Meta:
        model = Contract
        fields = [
            'id',
            'client',
            'date_created',
            'date_updated',
            'status',
            'event',
            'amount',
            'payment_due'
        ]

    def get_event(self, instance):
        if instance.event:
            queryset = Event.objects.filter(pk=instance.id)
            serializer = EventListSerializer(queryset, many=True)
            return serializer.data

    def get_client(self, instance):
        queryset = Client.objects.filter(pk=instance.id)
        serializer = ClientListSerializer(queryset, many=True)
        return serializer.data
