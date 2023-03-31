from django.urls import reverse, resolve

from crmapi.views.clientviewset import ClientViewSet
from crmapi.views.contractviewset import ContractViewSet
from crmapi.views.eventviewset import EventViewSet


def test_client_url():

    url = reverse('client-list')
    assert resolve(url).view_name == 'client-list'
    assert resolve(url).func, ClientViewSet


def test_contract_url():

    url = reverse('contract-list')
    assert resolve(url).view_name == 'contract-list'
    assert resolve(url).func, ContractViewSet


def test_event_url():

    url = reverse('event-list')
    assert resolve(url).view_name == 'event-list'
    assert resolve(url).func, EventViewSet
