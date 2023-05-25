"""
class Client

@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Client(models.Model):

    first_name = models.CharField(
        max_length=25,
        verbose_name='First name',
        blank=True
    )
    last_name = models.CharField(
        max_length=25,
        verbose_name='Last name'
    )
    email = models.EmailField(
        max_length=100,
        verbose_name='Email',
        unique=True
    )
    phone_number_regex = RegexValidator(
        regex='(0|\\+33|0033)[1-9][0-9]{8}'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Phone',
        blank=True,
        validators=[phone_number_regex]
    )
    mobile = models.CharField(
        max_length=20,
        verbose_name='Mobile',
        blank=True,
        validators=[phone_number_regex]
    )
    company_name = models.CharField(
        max_length=250,
        verbose_name='Compagny name',
        blank=False,
        unique=True,

    )
    date_created = models.DateTimeField(
        verbose_name='Date created',
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        verbose_name='Date last update',
        auto_now=True
    )
    sales_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Sales contact',
        related_name='assigned_clients',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    confirmed = models.BooleanField(
        verbose_name='Confirmed client ?',
        default=False
    )
