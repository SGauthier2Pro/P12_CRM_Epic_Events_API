import pytest
from rest_framework.test import APIClient

from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


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
        last_name='test'
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

