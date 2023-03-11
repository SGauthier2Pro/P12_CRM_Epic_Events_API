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

    date_created = models.DateTimeField(
        verbose_name='Date created',
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        verbose_name='Date last update',
        auto_now=True
    )

    support_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Support contact',
        related_name='assigned_event',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    event_status = models.IntegerField(
        verbose_name='Event status',
        choices=EventStatus.choices,
        default=EventStatus.IN_DEVELOPMENT
    )
    attendees = models.IntegerField(
        verbose_name='Attendees',
        blank=True,
        null=True
    )
    event_date = models.DateTimeField(
        verbose_name='Event date',
        blank=True,
        null=True
    )
    notes = models.TextField(
        verbose_name='Notes',
        blank=True
    )

