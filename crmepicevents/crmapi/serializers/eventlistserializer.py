"""
serializer class for Event model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from ..models.event import Event
from django.contrib.auth.models import User


class EventListSerializer(ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id',
            'date_created',
            'date_updated',
            'support_contact',
            'event_status',
            'attendees',
            'event_date',
            'notes'
        ]

    def validate_support_contact(self, attributes):
        """
        Check if user belongs to Sales Group
        :param attributes:
        :return: attributes if from sales group
        """

        if attributes['support_contact']:
            support_contact = User.objects.get(
                pk=attributes['support_contact'].id
            )
            if support_contact.group != 6:
                raise serializers.ValidationError(
                    {"support contact":
                        "This employee doesn't belong to Support group"}
                )
            return attributes['support_contact']
