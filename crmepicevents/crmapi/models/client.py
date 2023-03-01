"""
class Client

@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.db import models
from django.conf import settings


class Client(models.Model):

    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(max_length=20)
    mobile = models.IntegerField(max_length=20)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    sales_contact = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE)

