"""
serializer class for Event model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from .eventbaseserializer import EventBaseSerializer

from crmapi.models.event import Event


class EventListSerializer(EventBaseSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id',
            'event_client_id',
            'event_contract_id',
            'date_created',
            'date_updated',
            'support_contact',
            'event_status',
            'attendees',
            'event_date',
            'notes'
        ]
