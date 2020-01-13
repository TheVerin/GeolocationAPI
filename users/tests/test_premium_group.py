from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestPremiumGroupPublic(TestCase):

    def setUp(self) -> None:
        self.join_premium = reverse('join-premium')
        self.leave_premium = reverse('leave-premium')
        self.client = APIClient()

    def test_login_required(self):
        response = self.client.get(self.join_premium)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPremiumGroupPrivate(TestCase):

    def setUp(self) -> None:
        self.JOIN_PREMIUM = reverse('join-premium')
        self.LEAVE_PREMIUM = reverse('leave-premium')
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'supersecretpassword'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

        Group.objects.create(name='Premium')

    def test_join_and_leave_premium(self):
        response = self.client.get(self.JOIN_PREMIUM)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'User successfully upgraded to Premium')
        self.assertTrue(self.user.groups.filter(name='Premium'))

        response = self.client.get(self.LEAVE_PREMIUM)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'User successfully leave Premium')
        self.assertFalse(self.user.groups.filter(name='Premium'))
