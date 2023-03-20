"""
class Contract

@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.db import models


class Contract(models.Model):

    client = models.ForeignKey(
        'crmapi.Client',
        verbose_name='Client',
        related_name='contracts',
        on_delete=models.CASCADE,
        null=False
    )
    date_created = models.DateTimeField(
        verbose_name='Date created',
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        verbose_name='Date last update',
        auto_now=True
    )
    status = models.BooleanField(
        verbose_name='Signed ?',
        default=False
    )
    event = models.ForeignKey(
        'crmapi.Event',
        verbose_name='Event',
        related_name='contract_event',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    amount = models.FloatField(
        verbose_name='Amount',
        default='0.0'
    )
    payment_due = models.DateField(
        verbose_name='Date of payment',
        null=True,
        blank=True
    )
