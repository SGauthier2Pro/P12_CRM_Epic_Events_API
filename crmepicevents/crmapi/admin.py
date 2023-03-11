from django.contrib import admin

from crmapi.models.client import Client
from crmapi.models.contract import Contract
from crmapi.models.event import Event

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
