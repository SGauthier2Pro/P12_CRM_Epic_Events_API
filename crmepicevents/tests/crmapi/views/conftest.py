import pytest
from rest_framework.test import APIClient

from django.contrib.auth.models import User, Group
from crmapi.models.client import Client
from crmapi.models.contract import Contract
from crmapi.models.event import Event


@pytest.fixture
def client():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def get_manager_user():
    user = User.objects.create_user(
        username='managertest',
        password='P@s$4TestAp1',
        email='managertest@test.net',
        first_name='manager',
        last_name='test',
        is_staff=True,
        is_superuser=True
    )
    group = Group.objects.get(name='MANAGER')
    group.user_set.add(user)
    return user


@pytest.fixture
def get_support_user():
    user = User.objects.create_user(
        username='supporttest',
        password='P@s$4TestAp1',
        email='supporttest@test.net',
        first_name='support',
        last_name='test'
    )
    group = Group.objects.get(name='SUPPORT')
    group.user_set.add(user)
    return user


@pytest.fixture
def get_sales_user():
    user = User.objects.create_user(
        username='salestest',
        password='P@s$4TestAp1',
        email='salestest@test.net',
        first_name='sales',
        last_name='test'
    )
    group = Group.objects.get(name='SALES')
    group.user_set.add(user)
    return user


@pytest.fixture
def get_datas():

    user_manager = User.objects.create_user(
        username='managertest',
        password='P@s$4TestAp1',
        email='managertest@test.net',
        first_name='manager',
        last_name='test',
        is_staff=True,
        is_superuser=True
    )
    group = Group.objects.get(name='MANAGER')
    group.user_set.add(user_manager)

    user_support = User.objects.create_user(
        username='supporttest',
        password='P@s$4TestAp1',
        email='supporttest@test.net',
        first_name='support',
        last_name='test'
    )
    group = Group.objects.get(name='SUPPORT')
    group.user_set.add(user_support)

    user_support2 = User.objects.create_user(
        username='supporttest2',
        password='P@s$4TestAp1',
        email='supporttest2@test.net',
        first_name='support',
        last_name='test2'
    )
    group = Group.objects.get(name='SUPPORT')
    group.user_set.add(user_support2)

    user_sales = User.objects.create_user(
        username='salestest',
        password='P@s$4TestAp1',
        email='salestest@test.net',
        first_name='sales',
        last_name='test'
    )
    group = Group.objects.get(name='SALES')
    group.user_set.add(user_sales)

    user_sales2 = User.objects.create_user(
        username='salestest2',
        password='P@s$4TestAp1',
        email='salestest2@test.net',
        first_name='sales',
        last_name='test2'
    )
    group = Group.objects.get(name='SALES')
    group.user_set.add(user_sales2)

    client1 = Client.objects.create(
        first_name='client',
        last_name='1',
        email='client1@client1.net',
        phone='0123456789',
        mobile='0612345978',
        company_name='Client1 Corp',
        sales_contact=user_sales,
        confirmed=True
    )

    client2 = Client.objects.create(
        first_name='client',
        last_name='2',
        email='client2@client2.net',
        phone='0123456789',
        mobile='0612345978',
        company_name='Client2 Corp',
        sales_contact=user_sales
    )

    client3 = Client.objects.create(
        first_name='client',
        last_name='3',
        email='client3@client3.net',
        phone='0123456789',
        mobile='0612345978',
        company_name='Client3 Corp'
    )

    contract1 = Contract.objects.create(
        client=client1,
        status=True,
        payment_due='2023-04-27'
    )

    contract2 = Contract.objects.create(
        client=client2,
        payment_due='2023-07-12'
    )

    event1 = Event.objects.create(
        attendees=110,
        event_date='2024-07-12',
        support_contact=user_support
    )

    contract3 = Contract.objects.create(
        client=client1,
        status=True,
        event=event1,
        payment_due='2023-07-12'
    )

    return locals()
