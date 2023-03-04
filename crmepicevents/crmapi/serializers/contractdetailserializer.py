"""
serializer details class for Contract model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from .eventlistserializer import EventListSerializer
from .clientlistserializer import ClientListSerializer

from ..models.contract import Contract


class ContractDetailSerializer(ModelSerializer):
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
            queryset = instance.event.all()
            serializer = EventListSerializer(queryset, many=True)
            return serializer.data

    def get_client(self, instance):
        queryset = instance.client.all()
        serializer = ClientListSerializer(queryset, many=True)
        return serializer.data
