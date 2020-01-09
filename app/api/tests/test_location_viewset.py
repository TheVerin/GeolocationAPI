from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from unittest.mock import patch

from ..models import location
from ..serializers import location_serializer


ALL_MOVIES_URL = reverse('location')
