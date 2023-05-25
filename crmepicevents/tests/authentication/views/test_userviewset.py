import pytest
from rest_framework import status


class TestUserViewSet:

    endpoint = '/users/'

    def get_token(self, client, user):
        response = client.post(
            '/login/',
            data={
                'username': user.username,
                'password': 'P@s$4TestAp1'
            },
            format='json'
        )
        if response.status_code == status.HTTP_200_OK:
            token = response.data['access']
            return token

    @pytest.mark.django_db
    def test_get_users_list_with_manager_credentials(
            self, client, get_manager_user):

        user = get_manager_user

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)
        content = response.content.decode()
        expected_content = '"password":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_users_list_with_sales_credentials(
            self, client, get_sales_user):
        user = get_sales_user

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)
        content = response.content.decode()
        expected_content = '"password":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content not in content

    @pytest.mark.django_db
    def test_get_users_list_with_support_credentials(
            self, client, get_support_user):
        user = get_support_user

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)
        content = response.content.decode()
        expected_content = '"password":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content not in content
