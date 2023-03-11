"""
serializer details class for Event model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from authentication.serializers.userlistserializer import UserListSerializer
from crmapi.models.event import Event


class EventDetailSerializer(ModelSerializer):
    id = serializers.ReadOnlyField()

    support_contact = SerializerMethodField()

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

    def get_support_contact(self, instance):
        queryset = instance.support_contact.all()
        serializer = UserListSerializer(queryset, many=True)
        return serializer.data



