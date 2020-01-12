from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.test import TestCase


JOIN_PREMIUM = '/users/join-premium/'
LEAVE_PREMIUM = '/users/leave-premium/'


class TestPremiumGroupPublic(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login_required(self):
        response = self.client.get(JOIN_PREMIUM)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPremiumGroupPrivate(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'supersecretpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        Group.objects.create(name='Premium')

    def test_join_and_leave_premium(self):
        response = self.client.get(JOIN_PREMIUM)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'User successfully upgraded to Premium')
        self.assertTrue(self.user.groups.filter(name='Premium'))

        response = self.client.get(LEAVE_PREMIUM)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'User successfully leave Premium')
        self.assertFalse(self.user.groups.filter(name='Premium'))
