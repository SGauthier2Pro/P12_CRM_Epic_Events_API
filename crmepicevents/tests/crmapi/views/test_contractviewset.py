import pytest
from rest_framework import status
import datetime


class TestContractViewSet:

    endpoint = '/contracts/'

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

    # GET /contracts/
    @pytest.mark.django_db
    def test_get_contracts_list_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        content = response.content.decode()
        expected_content1 = '"client":'
        expected_content2 = '"event":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_contracts_list_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        content = response.content.decode()
        expected_content1 = '"client":'
        expected_content2 = '"event":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_contracts_list_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        content = response.content.decode()
        expected_content1 = '"client":'
        expected_content2 = '"event":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_contracts_list_with_unknown_credentials(
            self, client):
        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # GET /contracts/ ?search=
    @pytest.mark.django_db
    def test_get_contracts_list_with_search_on_client_company_name(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client1']

        request = (self.endpoint + '?company_name=' + client_test.company_name)

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"client":' + str(client_test.id)

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_contracts_list_with_search_on_client_email(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client1']

        request = (self.endpoint + '?client_email=' + client_test.email)

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"client":' + str(client_test.id)

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_contracts_list_with_search_on_amount(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract1']

        request = self.endpoint + '?amount=' + str(int(contract_test.amount))

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"amount":' + str(contract_test.amount)

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_contracts_list_with_search_on_date_created(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract1']
        date_to_test = contract_test.date_created.strftime("%d-%m-%Y")

        request = self.endpoint + '?date_created=' + date_to_test

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"date_created":"' + date_to_test

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    # GET /contracts/{pk}
    @pytest.mark.django_db
    def test_get_contracts_details_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract3']

        request = (self.endpoint + str(contract_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"client":[{"id":'
        expected_content2 = '"event":[{"id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_contracts_details_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        contract_test = get_datas['contract3']

        request = (self.endpoint + str(contract_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"client":[{"id":'
        expected_content2 = '"event":[{"id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_contracts_details_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        contract_test = get_datas['contract3']

        request = (self.endpoint + str(contract_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"client":[{"id":'
        expected_content2 = '"event":[{"id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_contracts_details_with_unknown_credentials(
            self, client, get_datas):

        contract_test = get_datas['contract1']

        request = (self.endpoint + str(contract_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.get(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_contracts_details_with_unknown_contract_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + '4300/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # CREATE /contract/
    @pytest.mark.django_db
    def test_create_contracts_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client2']

        contract_data = {
            'client': client_test.id,
            'amount': '400.0',
            'payment_due': '29-03-2025'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_create_contracts_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        client_test = get_datas['client2']

        contract_data = {
            'client': client_test.id,
            'amount': '400.0',
            'payment_due': '29-03-2025'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_create_contracts_with_not_sales_contact_client(
            self, client, get_datas):
        user = get_datas['user_sales2']
        client_test = get_datas['client2']

        contract_data = {
            'client': client_test.id,
            'amount': '400.0',
            'payment_due': '29-03-2025'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"message":' \
                           '"you are not sales contact for this client !"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_contracts_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        client_test = get_datas['client2']

        contract_data = {
            'client': client_test.id,
            'amount': '400.0',
            'payment_due': '29-03-2025'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )
        content = response.content.decode()
        expected_content = '"message":' \
                           '"you are not authorized to do this action"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_contracts_with_unknown_credentials(
            self, client, get_datas):

        client_test = get_datas['client2']

        contract_data = {
            'client': client_test.id,
            'amount': '400.0',
            'payment_due': '29-03-2025'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_contracts_without_client(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_data = {
            'amount': '400.0',
            'payment_due': '29-03-2025'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"client":"This field is needed !"'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_contracts_with_not_existing_client_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_data = {
            'client': 654654654,
            'amount': '400.0',
            'payment_due': '29-03-2025'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"client":"This client id does not exists !"'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_contracts_without_payment_due(
            self, client, get_datas):
        user = get_datas['user_manager']
        client_test = get_datas['client2']

        contract_data = {
            'client': client_test.id,
            'amount': '400.0',
            'payment_due': '01-01-1900'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"payment_due":null'

        assert response.status_code == status.HTTP_201_CREATED
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_contracts_with_payment_due_older_than_now(
            self, client, get_datas):
        user = get_datas['user_manager']
        client_test = get_datas['client2']

        contract_data = {
            'client': client_test.id,
            'amount': '400.0',
            'payment_due': '01-09-2022'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=contract_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"payment_due : ' \
                           'You can not choose an older date than now."'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    # UPDATE /contracts/
    @pytest.mark.django_db
    def test_update_contracts_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        contract_data_to_update = {
            'status': 'True'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"status":true'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_contracts_with_client_sales_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        contract_data_to_update = {
            'status': 'True'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"status":true'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_contracts_with_not_client_sales_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_sales2']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        contract_data_to_update = {
            'status': 'True'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_contracts_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        contract_data_to_update = {
            'status': 'True'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_contracts_with_unknown_credentials(
            self, client, get_datas):
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        contract_data_to_update = {
            'status': 'True'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_contracts_with_not_existing_contract_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + '4300/'

        contract_data_to_update = {
            'status': 'True'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_contracts_with_bad_contract_id_type(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + 'hf/'

        contract_data_to_update = {
            'status': 'True'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_update_contracts_with_default_payment_due(
            self, client, get_datas):
        user = get_datas['user_sales']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        contract_data_to_update = {
            'payment_due': '01-01-1900'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        date_to_test = datetime.datetime.strptime(
            contract_test.payment_due, '%Y-%m-%d')
        content = response.content.decode()
        expected_content = '"payment_due":"' + \
                           date_to_test.strftime('%d-%m-%Y') + '"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_contracts_with_payment_due_older_than_now(
            self, client, get_datas):
        user = get_datas['user_sales']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        contract_data_to_update = {
            'payment_due': '01-01-2022'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=contract_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"payment_due : ' \
                           'You can not choose an older date than now."'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    # DELETE /contracts/{pk}
    @pytest.mark.django_db
    def test_delete_contracts_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        content = response.content.decode()
        expected_content = '"success":"The contract has been deleted"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_delete_contracts_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        content = response.content.decode()
        expected_content = '"message":' \
                           '"you are not authorized to do this action"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_delete_contracts_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        content = response.content.decode()
        expected_content = '"message":' \
                           '"you are not authorized to do this action"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_delete_contracts_with_unknown_credentials(
            self, client, get_datas):
        contract_test = get_datas['contract1']

        request = self.endpoint + str(contract_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')

        response = client.delete(
            request
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_delete_contracts_with_not_existing_contract_id(
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
    def test_delete_contracts_with_bad_contract_id_type(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + 'hf/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
