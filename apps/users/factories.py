import factory

from .models import User, Company, Address, Coordinates


USER_TESTING_PASSWORD = 'testPass123'


class CompanyFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'J-company{n}')
    catchPhrase = factory.Sequence(lambda n: f'test-client-server{n}')
    bs = factory.Sequence(lambda n: f'test-real-time{n}')

    class Meta:
        model = Company


class UserFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'John Doe{n}')
    username = factory.Sequence(lambda n: f'John.D{n}')
    email = factory.Sequence(lambda n: f'john.doe{n}@test.com')
    phone = factory.Sequence(lambda n: f'{n}' * 5)
    website = factory.Sequence(lambda n: f'www.test_todo{n}.com')
    company = factory.SubFactory(CompanyFactory)
    password = factory.PostGenerationMethodCall('set_password', USER_TESTING_PASSWORD)

    class Meta:
        model = User
        django_get_or_create = ('username',)  # because username is unique


class AddressFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    street = factory.Sequence(lambda n: f'test_street{n}')
    suite = factory.Sequence(lambda n: f'test_suite{n}')
    city = factory.Sequence(lambda n: f'Sin City{n}')
    zipcode = factory.Sequence(lambda n: f'{n}' * 3)

    class Meta:
        model = Address


class CoordinatesFactory(factory.django.DjangoModelFactory):
    lat = factory.Sequence(lambda n: f'{n}.{n}')
    lng = factory.Sequence(lambda n: f'-{n}.{n}')
    address = factory.SubFactory(AddressFactory)

    class Meta:
        model = Coordinates
