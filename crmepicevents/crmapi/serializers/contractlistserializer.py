"""
serializer class for Contract model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from ..models.contract import Contract


class ContractListSerializer(ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Contract
        fields = [
            'id',
            'client',
            'date_created',
            'date_updated',
            'status',
            'event_id',
            'amount',
            'payment_due'
        ]

