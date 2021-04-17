import json

import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import User

from .factories import CityFactory, CountryFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestUserAPI:
    endpoint = '/api/v1/users/'

    def test_retrieve(self, api_client):
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
        )
        retrieve_endpoint = f'{self.endpoint}{user.id}/'

        client = api_client()
        client.force_authenticate(user=user)

        response = client.get(retrieve_endpoint)

        response_data = json.loads(response.content)
        expected_response = {
            'id': 1,
            'username': 'johndoe',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'gender': 'male',
            'age': 30,
            'country': 1,
            'city': 1,
        }

        assert response.status_code == status.HTTP_200_OK
        assert response_data == expected_response

    def test_update(self, api_client):
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
        )
        update_endpoint = f'{self.endpoint}{user.id}/'

        client = api_client()
        client.force_authenticate(user=user)

        update_payload = {
            'id': 1,
            'username': 'doejohn',
            'first_name': 'Jane',
            'last_name': 'Does',
            'email': 'janedoes@test.com',
            'gender': 'female',
            'age': 31,
            'country': 1,
            'city': 1,
        }

        response = client.put(
            update_endpoint,
            content_type='application/json',
            data=json.dumps(update_payload),
        )
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert response_data == update_payload


class TestCountryAPI:
    endpoint = '/api/v1/countries'

    def test_list(self, api_client):
        country = CountryFactory(name='Philippines')
        davao = CityFactory(name='Davao', country=country)
        manila = CityFactory(name='Manila', country=country)
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
            country=country,
            city=davao,
        )

        list_endpoint = self.endpoint

        client = api_client()
        client.force_authenticate(user=user)

        response = client.get(list_endpoint)
        response_data = json.loads(response.content)
        expected_response = [{
            'id': country.id,
            'name': country.name,
            'cities': [
                {
                    'id': davao.id,
                    'name': davao.name,
                },
                {
                    'id': manila.id,
                    'name': manila.name,
                },
            ],
        }]

        assert response.status_code == status.HTTP_200_OK
        assert response_data == expected_response


class TestLoginView:
    endpoint = '/api/v1/login'

    def test_successful_login_should_return_token_and_user_id(self, api_client):
        country = CountryFactory(name='Philippines')
        davao = CityFactory(name='Davao', country=country)
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
            country=country,
            city=davao,
        )
        user.set_password('password')
        user.save()

        client = api_client()
        response = client.post(
            self.endpoint,
            {
                'email': 'johndoe@test.com',
                'password': 'password',
            },
        )
        response_data = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response_data
        assert response_data['user_id'] == user.id

    def test_invalid_login_should_raise_error(self, api_client):
        country = CountryFactory(name='Philippines')
        davao = CityFactory(name='Davao', country=country)
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
            country=country,
            city=davao,
        )
        user.set_password('password')
        user.save()

        client = api_client()
        response = client.post(
            self.endpoint,
            {
                'email': 'johndoe@test.com',
                'password': 'incorrectpasswd',
            },
        )
        response_data = json.loads(response.content)
        expected_response = {'non_field_errors': ['Unable to log in with provided credentials.']}

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data == expected_response


class TestLogoutView:
    endpoint = '/api/v1/logout'

    def test_valid_logout_should_return_ok(self, api_client):
        country = CountryFactory(name='Philippines')
        davao = CityFactory(name='Davao', country=country)
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
            country=country,
            city=davao,
        )
        user.set_password('password')
        user.save()
        Token.objects.create(user=user)

        client = api_client()
        client.force_authenticate(user=user)

        response = client.get(self.endpoint)

        assert response.status_code == status.HTTP_200_OK

    def test_invalid_logout_should_raise_error(self, api_client):
        country = CountryFactory(name='Philippines')
        davao = CityFactory(name='Davao', country=country)
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
            country=country,
            city=davao,
        )
        user.set_password('password')
        user.save()
        Token.objects.create(user=user)

        client = api_client()

        response = client.get(self.endpoint)
        response_data = json.loads(response.content)
        expected_response = {
            'detail': 'Authentication credentials were not provided.',
        }

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data == expected_response
