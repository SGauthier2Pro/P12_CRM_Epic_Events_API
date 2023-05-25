import datetime
import pytest
from rest_framework import status


class TestEventViewSet:

    endpoint = '/events/'

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

    # GET /events/
    @pytest.mark.django_db
    def test_get_events_list_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        content = response.content.decode()
        expected_content1 = '"event_client_id":'
        expected_content2 = '"event_contract_id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_events_list_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        content = response.content.decode()
        expected_content1 = '"event_client_id":'
        expected_content2 = '"event_contract_id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_events_list_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(self.endpoint)

        content = response.content.decode()
        expected_content1 = '"event_client_id":'
        expected_content2 = '"event_contract_id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_events_list_with_unknown_credentials(
            self, client):
        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # GET /contracts/ ?search=
    @pytest.mark.django_db
    def test_get_events_list_with_search_on_client_company_name(
            self, client, get_datas):

        user = get_datas['user_manager']

        client_test = get_datas['client1']

        request = self.endpoint + '?company_name=' + client_test.company_name

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        print(content)
        expected_content = '"event_client_id":' + str(client_test.id)

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_events_list_with_search_on_event_client_email(
            self, client, get_datas):
        user = get_datas['user_manager']

        client_test = get_datas['client1']

        request = self.endpoint + '?client_email=' + client_test.email

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"event_client_id":' + str(client_test.id)

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_get_events_list_with_search_on_event_date(
            self, client, get_datas):
        user = get_datas['user_manager']

        event_test = get_datas['event1']

        date_to_test = datetime.datetime.strptime(
            event_test.event_date,
            "%Y-%m-%d"
        )

        request = self.endpoint + '?event_date=' + \
            date_to_test.strftime("%d-%m-%Y")

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)
        content = response.content.decode()
        expected_content = '"event_date":"' + date_to_test.strftime("%d-%m-%Y")

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    # GET /events/{pk}
    @pytest.mark.django_db
    def test_get_events_details_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        event_test = get_datas['event1']

        request = (self.endpoint + str(event_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"event_client":[{"id":'
        expected_content2 = '"event_contract":[{"id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_events_details_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        event_test = get_datas['event1']

        request = (self.endpoint + str(event_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"event_client":[{"id":'
        expected_content2 = '"event_contract":[{"id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_events_details_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        event_test = get_datas['event1']

        request = (self.endpoint + str(event_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        content = response.content.decode()
        expected_content1 = '"event_client":[{"id":'
        expected_content2 = '"event_contract":[{"id":'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content1 in content
        assert expected_content2 in content

    @pytest.mark.django_db
    def test_get_events_details_with_unknown_credentials(
            self, client, get_datas):
        event_test = get_datas['event1']

        request = (self.endpoint + str(event_test.id) + '/')

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.get(request)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_get_events_details_with_not_existing_event_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + '4300/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_get_events_details_with_bad_event_id_type(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + 'hf/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))
        response = client.get(request)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # CREATE /events/
    @pytest.mark.django_db
    def test_create_events_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract1']

        support_user = get_datas['user_support']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '12-07-2025',
            'support_contact': support_user.id
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"event_contract_id":' + str(contract_test.id)

        assert response.status_code == status.HTTP_201_CREATED
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']

        contract_test = get_datas['contract1']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '2024-07-12'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"event_contract_id":' + str(contract_test.id)

        assert response.status_code == status.HTTP_201_CREATED
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_not_sales_contact_for_contract(
            self, client, get_datas):
        user = get_datas['user_sales2']

        contract_test = get_datas['contract1']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '2024-07-12'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"contract_id":"You are not sales contact for ' \
                           'this contract !"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']

        contract_test = get_datas['contract1']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '2024-07-12'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"message":' \
                           '"you are not authorized to do this action"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_unknown_credentials(
            self, client, get_datas):
        contract_test = get_datas['contract1']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '2024-07-12'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')
        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_events_without_contract(
            self, client, get_datas):
        user = get_datas['user_manager']

        event_data = {
            'attendees': 110,
            'event_date': '2024-07-12'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"contract_id":"You must enter a contract id !"'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_not_existing_contract_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        event_data = {
            'contract_id': 654654654,
            'attendees': 110,
            'event_date': '2024-07-12'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"contract_id":"This contract id does not exists !"'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_not_signed_contract(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract2']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '2024-07-12'
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"event_contract":' \
                           '"This contract is not signed yet !"'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_support_contact_not_support_team(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract1']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '2024-07-12',
            'support_contact': get_datas['user_sales'].id

        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"support_contact: This user does not ' \
                           'belong to SUPPORT Team."'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_no_event_date_value(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract1']

        support_user = get_datas['user_support']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '01-01-1900',
            'support_contact': support_user.id
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = 'event_date : You must enter a date for the event.'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_create_events_with_event_date_value_older_than_now(
            self, client, get_datas):
        user = get_datas['user_manager']

        contract_test = get_datas['contract1']

        support_user = get_datas['user_support']

        event_data = {
            'contract_id': contract_test.id,
            'attendees': 110,
            'event_date': '01-10-1900',
            'support_contact': support_user.id
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.post(
            self.endpoint,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = 'event_date : ' \
                           'You can not choose an older date than now.'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    # UPDATE /events/
    @pytest.mark.django_db
    def test_update_events_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"attendees":120'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_events_with_client_sales_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"attendees":120'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_events_with_client_not_sales_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_sales2']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_update_events_with_support_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_support']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )
        content = response.content.decode()
        expected_content = '"attendees":120'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_events_with_not_support_contact_credentials(
            self, client, get_datas):
        user = get_datas['user_support2']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )
        content = response.content.decode()
        expected_content = '"message":"you are not' \
                           ' authorized to do this action"'

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_events_with_no_credentials(
            self, client, get_datas):
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_update_events_with_not_existing_event_id(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + '4300/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_events_with_bad_event_id_type(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + 'hf/'

        event_data_to_update = {
            'attendees': 120
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_update_events_support_contact_attribute_support_team(
            self, client, get_datas):
        user = get_datas['user_manager']
        event_test = get_datas['event1']
        support_contact_to_test = get_datas['user_support2']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'support_contact': support_contact_to_test.id
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = '"support_contact":'\
                           + str(support_contact_to_test.id)

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_events_support_contact_attribute_sales_team(
            self, client, get_datas):
        user = get_datas['user_manager']
        event_test = get_datas['event1']
        support_contact_to_test = get_datas['user_sales']

        request = self.endpoint + str(event_test.id) + '/'

        event_data_to_update = {
            'support_contact': support_contact_to_test.id
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data_to_update,
            format='json'
        )

        content = response.content.decode()
        expected_content = "support_contact: This user does" \
                           " not belong to SUPPORT Team."

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_events_with_event_date_value_older_than_now(
            self, client, get_datas):
        user = get_datas['user_manager']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data = {
            'event_date': '01-10-1900',
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data,
            format='json'
        )

        content = response.content.decode()
        expected_content = 'event_date : ' \
                           'You can not choose an older date than now.'

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_content in content

    @pytest.mark.django_db
    def test_update_events_with_no_event_date_value(
            self, client, get_datas):
        user = get_datas['user_manager']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        event_data = {
            'event_date': '01-01-1900',
        }

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.put(
            request,
            data=event_data,
            format='json'
        )

        date_to_test = datetime.datetime.strptime(
            event_test.event_date, '%Y-%m-%d')
        content = response.content.decode()
        expected_content = '"event_date":"' + \
                           date_to_test.strftime('%d-%m-%Y') + '"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    # DELETE /events/{pk}
    @pytest.mark.django_db
    def test_delete_events_with_manager_credentials(
            self, client, get_datas):
        user = get_datas['user_manager']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        content = response.content.decode()
        expected_content = '"success":"The event has been deleted"'

        assert response.status_code == status.HTTP_200_OK
        assert expected_content in content

    @pytest.mark.django_db
    def test_delete_events_with_sales_credentials(
            self, client, get_datas):
        user = get_datas['user_sales']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

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
    def test_delete_events_with_support_credentials(
            self, client, get_datas):
        user = get_datas['user_support']
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

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
    def test_delete_events_with_unknown_credentials(
            self, client, get_datas):
        event_test = get_datas['event1']

        request = self.endpoint + str(event_test.id) + '/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ')

        response = client.delete(
            request
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_delete_events_with_not_existing_event_id(
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
    def test_delete_events_with_bad_event_id_type(
            self, client, get_datas):
        user = get_datas['user_manager']

        request = self.endpoint + 'hf/'

        client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.get_token(client, user))

        response = client.delete(
            request
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
