"""
serializer class for Client model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth.models import User

from ..models.client import Client


class ClientListSerializer(ModelSerializer):
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
            'sales_contact',
        ]
        read_only_fields = [
            'id',
            'company_name'
        ]

        def validate_sales_contact(self, attributes):
            """
            Check if user belongs to Sales Group
            :param attributes:
            :return: attributes if from sales group
            """

            if attributes['sales_contact']:
                sales_contact = User.objects.get(
                    pk=attributes['sales_contact'].id
                )
                if sales_contact.group != 5:
                    raise serializers.ValidationError(
                        {"sales contact":
                            "This employee doesn't belong to Sales group"}
                    )
                return attributes['sales_contact']
