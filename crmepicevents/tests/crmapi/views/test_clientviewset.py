import pytest
from rest_framework import status

from crmapi.models.client import Client


class TestClientViewSet:

    endpoint = '/clients/'

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

    # GET /clients/
    @pytest.mark.django_db
    def test_get_clients_list_with_manager_credentials(
            self, client, get_datas):

        user = get_datas['user_manager']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_clients_list_with_support_credentials(
            self, client, get_datas):

        user = get_datas['user_support']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_clients_list_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_get_clients_list_with_unknown_credentials(
            self, client):

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # GET /clients/ ?searh=
    @pytest.mark.django_db
    def test_get_clients_list_with_search_on_company_name(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client1']

        request = (self.endpoint + '?company_name=' + client_test.company_name)

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"company_name":"' + client_test.company_name + '"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_clients_list_with_search_on_email(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client2']

        request = (self.endpoint + '?email=' + client_test.email)

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"email":"' + client_test.email + '"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_clients_list_with_search_on_non_search_field_value(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client2']

        request = (self.endpoint + '?search=' + client_test.phone)

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"count":0'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    # GET /client/ details
    @pytest.mark.django_db
    def test_get_clients_details_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client1']

        request = (self.endpoint + str(client_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content1 = '"id":' + str(client_test.id)
        expected_content2 = '"contracts":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_clients_details_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        client_test = get_datas['client1']

        request = (self.endpoint + str(client_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"id":' + str(client_test.id)
        expected_content2 = '"contracts":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_clients_details_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        client_test = get_datas['client1']

        request = (self.endpoint + str(client_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"id":' + str(client_test.id)
        expected_content2 = '"contracts":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_clients_details_with_unknown_credentials(
            self, client, get_datas):

        client_test = get_datas['client1']

        request = (self.endpoint + str(client_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.get(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_clients_details_with_unknown_client_id(
            self, client, get_datas):
        user = get_datas['user_sales']

        request = self.endpoint + '4300/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # CREATE /client/
    @pytest.mark.django_db
    def test_create_clients_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_data = {
            'first_name': 'client',
            'last_name': '4',
            'email': 'client4@client4.net',
            'phone': '0123456789',
            'mobile': '0612345978',
            'company_name': 'Client4 Corp'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=client_data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_create_clients_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        client_data = {
            'first_name': 'client',
            'last_name': '4',
            'email': 'client4@client4.net',
            'phone': '0123456789',
            'mobile': '0612345978',
            'company_name': 'Client4 Corp'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=client_data,
            format='json'
        )

        client_test = Client.objects.get(company_name='Client4 Corp')

        assert response.status_code == status.HTTP_201_CREATED
        assert client_test.sales_contact == user

    @pytest.mark.django_db
    def test_create_clients_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        client_data = {
            'first_name': 'client',
            'last_name': '4',
            'email': 'client4@client4.net',
            'phone': '0123456789',
            'mobile': '0612345978',
            'company_name': 'Client4 Corp'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=client_data,
            format='json'
        )
        content = response.content.decode()
        expected_content = '"message":' \
                           '"you are not authorized to do this action"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_clients_with_unknown_credentials(
            self, client):

        client_data = {
            'first_name': 'client',
            'last_name': '4',
            'email': 'client4@client4.net',
            'phone': '0123456789',
            'mobile': '0612345978',
            'company_name': 'Client4 Corp'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.post(
            self.endpoint,
            data=client_data,
            format='json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_clients_without_company_name(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_data = {
            'first_name': 'client',
            'last_name': '4',
            'email': 'client4@client4.net',
            'phone': '0123456789',
            'mobile': '0612345978',
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=client_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"company_name":' \
                           '["Ce champ est obligatoire."]'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_clients_without_good_phone(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_data = {
            'first_name': 'client',
            'last_name': '4',
            'email': 'client4@client4.net',
            'phone': '012456789',
            'mobile': '0612345978',
            'company_name': 'Client4 Corp'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=client_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"phone":' \
                           '["Saisissez une valeur valide."]'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_clients_without_good_mobile(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_data = {
            'first_name': 'client',
            'last_name': '4',
            'email': 'client4@client4.net',
            'phone': '0123456789',
            'mobile': '062345978',
            'company_name': 'Client4 Corp'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=client_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"mobile":' \
                           '["Saisissez une valeur valide."]'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    # UPDATE /client/{pk}/

    @pytest.mark.django_db
    def test_update_clients_with_manager_credentials(
            self, client, get_datas):

        user = get_datas['user_manager']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'mobile': '0698754312'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"mobile":"0698754312"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_clients_with_self_sales_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'mobile': '0698754312'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"mobile":"0698754312"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_clients_with_not_self_sales_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_sales2']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'mobile': '0698754312'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_clients_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'mobile': '0698754312'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_clients_with_unknown_credentials(
            self, client, get_datas):
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'mobile': '0698754312'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_clients_with_bad_phone_number(
            self, client, get_datas):
        user = get_datas['user_manager']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'phone': '069875412'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"phone":' \
                           '["Saisissez une valeur valide."]'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_clients_with_bad_mobile_number(
            self, client, get_datas):
        user = get_datas['user_manager']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'mobile': '069875412'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"mobile":' \
                           '["Saisissez une valeur valide."]'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_clients_with_wrong_sales_contact(
            self, client, get_datas):
        user = get_datas['user_manager']
        client_test = get_datas['client1']
        support_user = get_datas['user_support2']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'sales_contact': support_user.id
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '{"sales_contact":{"sales_contact":' \
                           '"This employee does not belong to Sales group"}}'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_clients_with_good_sales_contact(
            self, client, get_datas):
        user = get_datas['user_manager']
        client_test = get_datas['client1']
        sales_user = get_datas['user_sales']

        request = self.endpoint + str(client_test.id) + '/'

        client_data_to_update = {
            'sales_contact': sales_user.id
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"sales_contact":' + str(sales_user.id)

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_clients_with_not_existing_client_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + '4300/'

        client_data_to_update = {
            'mobile': '0698754123'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_clients_with_bad_client_id_type(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + 'hf/'

        client_data_to_update = {
            'mobile': '0698754123'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=client_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # DELETE /clients/{pk}/

    @pytest.mark.django_db
    def test_delete_clients_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        content = response.content.decode()
        expected_content = '"success":"The client has been deleted"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_delete_clients_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        content = response.content.decode()
        expected_content = '"message":' \
                           '"You are not authorized to delete a client"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_delete_clients_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        content = response.content.decode()
        expected_content = '"message":' \
                           '"You are not authorized to delete a client"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_delete_clients_with_unknown_credentials(
            self, client, get_datas):
        client_test = get_datas['client1']

        request = self.endpoint + str(client_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')

        response = client.delete(
            request
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_delete_clients_with_not_existing_client_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + '4300/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_delete_clients_with_bad_client_id_type(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + 'hf/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
