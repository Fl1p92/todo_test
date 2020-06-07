from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import CoordinatesFactory, USER_TESTING_PASSWORD
from .models import User, Address, Coordinates, Company
from .serializers import UserSerializer


class UserAPIViewTest(APITestCase):
    """
    Test cases for users API endpoints.
    """

    def setUp(self):
        self.count = 10
        # Filled db by self.count entries of coordinates, address, company and users data
        for _ in range(self.count):
            CoordinatesFactory()
        self.test_user = CoordinatesFactory().address.user
        self.list_url = reverse('users-list')
        self.detail_url = reverse('users-detail')
        self.access_token = self.get_access_token()

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'),
                                    data={'username': self.test_user.username,
                                          'password': USER_TESTING_PASSWORD},
                                    format='json')
        return response.data['access']

    def test_user_list(self):
        # Unauthorized request
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.count + 1)
        self.assertEqual(User.objects.count(), self.count + 1)

    def test_retrieve_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data['id'], self.test_user.id)
        self.assertEqual(data['name'], self.test_user.name)
        self.assertEqual(data['username'], self.test_user.username)
        self.assertEqual(data['email'], self.test_user.email)
        self.assertEqual(data['address']['street'], self.test_user.address.street)
        self.assertEqual(data['address']['suite'], self.test_user.address.suite)
        self.assertEqual(data['address']['city'], self.test_user.address.city)
        self.assertEqual(data['address']['zipcode'], self.test_user.address.zipcode)
        self.assertEqual(data['address']['geo']['lat'], self.test_user.address.geo.lat)
        self.assertEqual(data['address']['geo']['lng'], self.test_user.address.geo.lng)
        self.assertEqual(data['phone'], self.test_user.phone)
        self.assertEqual(data['website'], self.test_user.website)
        self.assertEqual(data['company']['name'], self.test_user.company.name)
        self.assertEqual(data['company']['catchPhrase'], self.test_user.company.catchPhrase)
        self.assertEqual(data['company']['bs'], self.test_user.company.bs)

    def test_update_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # test mass update via put
        put_data = {
            'name': 'New test name',
            'username': 'test_username',
            'email': 'new_data@test.com',
            'address': {
                'street': 'street 123',
                'suite': 'suite123',
                'city': 'city123',
                'zipcode': '99999',
                'geo': {
                    'lat': '44.4444',
                    'lng': '55.5555',
                },
            },
            'phone': '1111111-1111111111',
            'website': 'www.new-website.com',
            'company': {
                'name': 'test company',
                'catchPhrase': 'test111',
                'bs': 'test2222',
            },
        }

        response = self.client.put(self.detail_url, data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.name, put_data['name'])
        self.assertEqual(self.test_user.username, put_data['username'])
        self.assertEqual(self.test_user.email, put_data['email'])
        self.assertEqual(self.test_user.address.street, put_data['address']['street'])
        self.assertEqual(self.test_user.address.suite, put_data['address']['suite'])
        self.assertEqual(self.test_user.address.city, put_data['address']['city'])
        self.assertEqual(self.test_user.address.zipcode, put_data['address']['zipcode'])
        self.assertEqual(self.test_user.address.geo.lat, put_data['address']['geo']['lat'])
        self.assertEqual(self.test_user.address.geo.lng, put_data['address']['geo']['lng'])
        self.assertEqual(self.test_user.phone, put_data['phone'])
        self.assertEqual(self.test_user.website, put_data['website'])
        self.assertEqual(self.test_user.company.name, put_data['company']['name'])
        self.assertEqual(self.test_user.company.catchPhrase, put_data['company']['catchPhrase'])
        self.assertEqual(self.test_user.company.bs, put_data['company']['bs'])

        # test partial update via patch
        patch_data = {
            'email': 'new_data_patch@test.com',
            'address': {
                'street': 'street Patch',
                'geo': {
                    'lat': '88.12345',
                },
            },
            'company': {
                'name': 'test PATCH company',
            },
        }

        response = self.client.patch(self.detail_url, data=patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.email, patch_data['email'])
        self.assertEqual(self.test_user.address.street, patch_data['address']['street'])
        self.assertEqual(self.test_user.address.geo.lat, patch_data['address']['geo']['lat'])
        self.assertEqual(self.test_user.company.name, patch_data['company']['name'])

    def test_create_user_by_serializer(self):
        raw_data = {
            'name': 'Test name',
            'username': 'serializer_name',
            'email': 'new_data@test.com',
            'address': {
                'street': 'street 123',
                'suite': 'suite123',
                'city': 'city123',
                'zipcode': '99999',
                'geo': {
                    'lat': '44.4444',
                    'lng': '55.5555',
                },
            },
            'phone': '1111111-1111111111',
            'website': 'www.new-website.com',
            'company': {
                'name': 'test company',
                'catchPhrase': 'test111',
                'bs': 'test2222',
            },
        }

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(Company.objects.count(), self.count + 1)
        self.assertEqual(Address.objects.count(), self.count + 1)
        self.assertEqual(Coordinates.objects.count(), self.count + 1)

        serializer = UserSerializer(data=raw_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertEqual(User.objects.count(), self.count + 2)
        self.assertEqual(Company.objects.count(), self.count + 2)
        self.assertEqual(Address.objects.count(), self.count + 2)
        self.assertEqual(Coordinates.objects.count(), self.count + 2)
