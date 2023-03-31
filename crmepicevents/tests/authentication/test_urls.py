from django.urls import reverse, resolve

from authentication.views.myobtaintokenpairview import MyObtainTokenPairView
from authentication.views.userviewset import UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView


def test_login_url():

    url = reverse('token_obtain_pair')
    assert resolve(url).view_name == 'token_obtain_pair'
    assert resolve(url).func.view_class, MyObtainTokenPairView


def test_refresh_url():

    url = reverse('token_refresh')
    assert resolve(url).view_name == 'token_refresh'
    assert resolve(url).func.view_class, TokenRefreshView


def test_users_url():

    url = reverse('users-list')
    assert resolve(url).view_name == 'users-list'
    assert resolve(url).func, UserViewSet

