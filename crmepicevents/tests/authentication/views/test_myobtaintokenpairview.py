import pytest
from rest_framework import status


class TestMyObtainTokenPairView:

    endpoint = '/login/'

    @pytest.mark.django_db
    def test_login_with_active_account(self, client, get_manager_user):

        user = get_manager_user

        response = client.post(
            self.endpoint,
            data={
                'username': user.username,
                'password': 'P@s$4TestAp1'
            },
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    @pytest.mark.django_db
    def test_login_with_unknown_account(self, client):
        username = 'notauser'
        password = 'not a password'

        response = client.post(
            self.endpoint,
            data={
                'username': username,
                'password': password
            },
            format='json'
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
