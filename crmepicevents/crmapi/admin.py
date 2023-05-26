from django.contrib import admin

from crmapi.models.client import Client
from crmapi.models.contract import Contract
from crmapi.models.event import Event


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_filter = ["confirmed", "sales_contact"]


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_filter = ["status"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ["support_contact"]
