from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from unittest.mock import patch

from api.models.location import Location
from api.serializers.location_serializer import LocationSerializer


class PublicGeolocationApiTest(TestCase):

    def setUp(self) -> None:
        self.get_location = reverse('get-list')
        self.create_location = reverse('create-list')
        self.client = APIClient()

    def test_login_required_get(self):
        response = self.client.get(self.get_location)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_required_create(self):
        response = self.client.get(self.create_location)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PrivateGeolocationkApiTest(TestCase):

    def setUp(self) -> None:
        self.get_location = reverse('get-list')
        self.create_location = reverse('create-list')
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'supersecretpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        for ip in ['1.1.1.1', '2606:4700:20::681a:754']:
            Location.objects.create(ip=ip)

        Location.objects.create(ip='1.2.3.4')

    def test_get_all_ips(self):

        response = self.client.get(self.get_location)
        from_db = Location.objects.all()
        serializer = LocationSerializer(from_db, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)





    @patch('api.views.IPStackHandler')
    def test_create_valid_ipv4(self, mock_ipstack_handler):
        payload = {
            'site': '2.2.2.2'
        }

        response = self.client.post(self.create_location, payload)

        from_db = Location.objects.latest('pk')
        serializer = LocationSerializer(from_db)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data['ip'], payload['site'])

    @patch('api.views.IPStackHandler')
    def test_create_valid_url(self, mock_ipstack_handler):
        payload = {
            'site': 'google.com'
        }

        response = self.client.post(self.create_location, payload)

        from_db = Location.objects.latest('pk')
        serializer = LocationSerializer(from_db)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data['url'], payload['site'])

    @patch('api.views.IPStackHandler')
    def test_create_valid_ipv6(self, mock_ipstack_handler):
        payload = {
            'site': '2606:4700:20::681a:654'
        }

        response = self.client.post(self.create_location, payload)

        from_db = Location.objects.latest('pk')
        serializer = LocationSerializer(from_db)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(serializer.data['ip'], payload['site'])

    @patch('api.views.IPStackHandler')
    def test_create_ip_already_in_db(self, mock_ipstack_handler):
        payload = {
            'site': '1.1.1.1'
        }
        response = self.client.post(self.create_location, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'IP already in db')

    @patch('api.views.IPStackHandler')
    def test_create_invalid_ipv4(self, mock_ipstack_handler):
        payload = {
            'site': '1234.2.3.4'
        }
        response = self.client.post(self.create_location, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Site does not exists')

    @patch('api.views.IPStackHandler')
    def test_create_invalid_ipv6(self, mock_ipstack_handler):
        payload = {
            'site': '26sss06:4sda700:2d0::68s1a:65a4'
        }
        response = self.client.post(self.create_location, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Site does not exists')

    @patch('api.views.IPStackHandler')
    def test_create_invalid_url(self, mock_ipstack_handler):
        payload = {
            'site': 'andnowalotofrandomcharactersasdhvbufohvwobuvhb.com'
        }
        response = self.client.post(self.create_location, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Site does not exists')

    @patch('api.views.IPStackHandler')
    def test_create_no_ip(self, mock_ipstack_handler):
        payload = {
            'site': ''
        }
        response = self.client.post(self.create_location, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Site does not exists')




    def test_delete_valid_ip(self):
        before = Location.objects.all().count()
        response = self.client.delete(reverse('delete-detail',
                                              kwargs={'ip': '1.2.3.4'}))
        after = Location.objects.all().count()
        is_existed = Location.objects.filter(ip='1.2.3.4').exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(is_existed)
        self.assertTrue(after < before)

    def test_delete_not_existed_ip(self):
        response = self.client.delete(reverse('delete-detail',
                                              kwargs={'ip': '1.2.3.42'}))
        self.assertTrue(response.status_code, status.HTTP_400_BAD_REQUEST)
