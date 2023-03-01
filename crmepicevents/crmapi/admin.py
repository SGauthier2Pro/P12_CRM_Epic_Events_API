from django.contrib import admin

from .models.client import Client
from .models.contract import Contract
from .models.event import Event

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
