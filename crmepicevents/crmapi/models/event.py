"""
class Event

@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.db import models
from django.conf import settings


class Event(models.Model):

    class EventStatus(models.Choices):
        IN_DEVELOPMENT = 0
        WAITING_CUSTOMER = 1
        ACTION_REQUIRED = 2
        TERMINATED = 3
        CANCELLED = 4

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()

    support_contact = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE)
    event_status = models.IntegerField(verbose_name="Event status",
                                       choices=EventStatus.choices,
                                       default=EventStatus.IN_DEVELOPMENT)
    attendees = models.IntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField()

