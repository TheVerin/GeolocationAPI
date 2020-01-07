import json

from django.test import TestCase

from rest_framework import status

from ..ipstack_handler import get_location_data


class ExternanApiTest(TestCase):

    def test_get_valid_site(self):
        with open('api/tests/example_ipstack_response.json') as json_file:
            example_data = json.loads(json_file.read())
            response_data = get_location_data('amazon.com')
            self.assertEqual(example_data, response_data)

    def test_get_invalid_site(self):
        response_data = get_location_data('itwouldbeveryfunnyifthereiswebsitelikethis.com')
        self.assertEqual(response_data, status.HTTP_404_NOT_FOUND)
