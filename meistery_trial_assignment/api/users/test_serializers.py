import pytest

from users.models import User

from . import serializers
from .factories import CityFactory, CountryFactory, UserFactory


class TestUserSerializer:
    pytestmark = pytest.mark.django_db

    def test_serializer_model(self):
        user = UserFactory(
            first_name='John',
            last_name='Doe',
            username='johndoe',
            email='johndoe@test.com',
            gender=User.MALE,
            age=30,
        )
        serializer = serializers.UserSerializer(user)

        expected_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'gender': User.MALE,
            'age': user.age,
            'id': user.id,
            'city': user.city.id,
            'country': user.country.id,
        }

        assert serializer.data == expected_data

    def test_valid_serializer_data(self):
        country = CountryFactory(name='Philippines')
        city = CityFactory(name='Davao', country=country)

        valid_serialized_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@test.com',
            'gender': User.MALE,
            'age': 30,
            'city': city.id,
            'country': country.id,
        }
        serializer = serializers.UserSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_invalid_serializer_data(self):
        country = CountryFactory(name='Philippines')
        city = CityFactory(name='Davao', country=country)

        invalid_serialized_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoeom',
            'gender': 'neutral',
            'age': 'one',
            'city': city.id,
            'country': country.id,
        }
        serializer = serializers.UserSerializer(data=invalid_serialized_data)

        assert serializer.is_valid() == False
        assert serializer.errors != {}


class TestCountrySerializer:
    pytestmark = pytest.mark.django_db

    def test_serializer_model(self):
        country = CountryFactory(name='Philippines')
        davao = CityFactory(name='Davao', country=country)
        manila = CityFactory(name='Manila', country=country)

        serializer = serializers.CountrySerializer(country)

        expected_data = {
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
        }

        assert serializer.data == expected_data

    def test_valid_serializer_data(self):
        country = CountryFactory(name='Philippines')
        city = CityFactory(name='Davao', country=country)

        valid_serialized_data = {
            'name': country.name,
        }

        serializer = serializers.CountrySerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_invalid_serializer_data(self):
        country = CountryFactory(name='Philippines')
        city = CityFactory(name='Davao', country=country)

        invalid_serialized_data = {
            'name': None,
        }

        serializer = serializers.CountrySerializer(data=invalid_serialized_data)

        assert serializer.is_valid() == False


class TestCitySerializer:
    pytestmark = pytest.mark.django_db

    def test_serializer_model(self):
        country = CountryFactory(name='Philippines')
        davao = CityFactory(name='Davao', country=country)

        serializer = serializers.CitySerializer(davao)

        expected_data = {
            'id': davao.id,
            'name': davao.name,
        }
        assert serializer.data == expected_data

    def test_valid_serializer_data(self):
        country = CountryFactory(name='Philippines')
        city = CityFactory(name='Davao', country=country)

        valid_serialized_data = {
            'name': city.name,
        }

        serializer = serializers.CitySerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}

    def test_invalid_serializer_data(self):
        country = CountryFactory(name='Philippines')
        city = CityFactory(name='Davao', country=country)

        invalid_serialized_data = {
            'name': None,
        }

        serializer = serializers.CitySerializer(data=invalid_serialized_data)

        assert serializer.is_valid() == False
