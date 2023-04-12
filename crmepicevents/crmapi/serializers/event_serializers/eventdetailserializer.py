"""
serializer details class for Event model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from rest_framework.serializers import SerializerMethodField
from rest_framework import serializers

from .eventbaseserializer import EventBaseSerializer

from authentication.serializers.userlistserializer import UserListSerializer
from crmapi.models.event import Event

from django.contrib.auth.models import User


class EventDetailSerializer(EventBaseSerializer):
    id = serializers.ReadOnlyField()

    support_contact = SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id',
            'event_client',
            'event_contract',
            'date_created',
            'date_updated',
            'support_contact',
            'event_status',
            'attendees',
            'event_date',
            'notes'
        ]

    def get_support_contact(self, instance):
        queryset = User.objects.filter(pk=instance.support_contact.id)
        serializer = UserListSerializer(queryset, many=True)
        return serializer.data



