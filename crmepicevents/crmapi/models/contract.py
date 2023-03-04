"""
class Contract

@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.db import models


class Contract(models.Model):

    client = models.ForeignKey('crmapi.Client',
                               on_delete=models.CASCADE,
                               null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    status = models.BooleanField(default=False)
    event = models.ForeignKey('crmapi.Event',
                              on_delete=models.CASCADE,
                              null=True)
    amount = models.FloatField(default='0.0')
    payment_due = models.DateTimeField()
