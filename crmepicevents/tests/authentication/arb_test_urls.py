import pytest

from django.urls import reverse, resolve
from authentication.views.myobtaintokenpairview import MyObtainTokenPairView


@pytest.mark.django_db
def test_login_url():

    url = reverse('token_obtain_pair')
    assert resolve(url).view_name == 'token_obtain_pair'
    assert resolve(url).func.view_class, MyObtainTokenPairView
