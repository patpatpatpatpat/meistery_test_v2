import factory

from users.models import City, Country, User


class CountryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'country {n}')

    class Meta:
        model = Country


class CityFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'city {n}')
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = City


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Sequence(lambda n: f'first {n}')
    last_name = factory.Sequence(lambda n: f'last {n}')
    username = factory.Sequence(lambda n: f'user{n}@example.com')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    gender = User.MALE
    age = 20
    is_staff = True
    is_superuser = True
    is_active = True
    country = factory.SubFactory(CountryFactory)
    city = factory.SubFactory(CityFactory)

    class Meta:
        model = User