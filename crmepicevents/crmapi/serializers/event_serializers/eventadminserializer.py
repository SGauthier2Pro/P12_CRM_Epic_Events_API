from .eventbaseserializer import EventBaseSerializer

from crmapi.models.event import Event


class EventAdminSerializer(EventBaseSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'support_contact',
            'date_created',
            'date_updated',
            'event_status',
            'attendees',
            'event_date',
            'notes'
        )
