"""
serializer class for Contract model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework import serializers

from .contractbaseserializer import ContractBaseSerializer

from crmapi.models.contract import Contract


class ContractListSerializer(ContractBaseSerializer):
    id = serializers.ReadOnlyField()

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

