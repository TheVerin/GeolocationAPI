import json

from django.test import TestCase

from api.tools.ipstack_handling import IPStackHandler


class ExternalApiTest(TestCase):

    def setUp(self) -> None:
        self.ip_handler = IPStackHandler()

    def test_ipv4_site(self):
        self.assertEqual(self.ip_handler._payload_validation('1.1.1.1'), ['1.1.1.1', 'ip'])

    def test_ipv6_site(self):
        self.assertEqual(self.ip_handler._payload_validation('2606:4700:20::681a:754'),
                         ['2606:4700:20::681a:754', 'ip'])

    def test_www_url_site(self):
        self.assertEqual(self.ip_handler._payload_validation('www.sofomo.com'),
                         ['www.sofomo.com', 'url'])

    def test_url_site(self):
        self.assertEqual(self.ip_handler._payload_validation('sofomo.com'),
                         ['sofomo.com', 'url'])

    def test_https_url_site(self):
        self.assertEqual(self.ip_handler._payload_validation('https://sofomo.com'),
                         ['sofomo.com', 'url'])

    def test_https_www_url_site(self):
        self.assertEqual(self.ip_handler._payload_validation('https://www.sofomo.com'),
                         ['www.sofomo.com', 'url'])

    def test_http_url_site(self):
        self.assertEqual(self.ip_handler._payload_validation('http://sofomo.com'),
                         ['sofomo.com', 'url'])

    def test_http_www_url_site(self):
        self.assertEqual(self.ip_handler._payload_validation('http://www.sofomo.com'),
                         ['www.sofomo.com', 'url'])

    def test_get_valid_ipv4_site(self):
        with open('api/tests/example_ipstack_response.json') as json_file:
            example_data = json.loads(json_file.read())
            response_data = self.ip_handler.get_location_data('176.32.103.205')
            self.assertEqual(example_data[0], response_data)

    def test_get_invalid_ipv4_site(self):
        response_data = self.ip_handler.get_location_data('1111.1111.1111.1111')
        self.assertEqual(response_data, False)

    def test_get_invalid_url_site(self):
        response_data = self.ip_handler.get_location_data('ibetthereisnowebsitelikethis.com')
        self.assertEqual(response_data, False)

    def test_get_valid_ipv6_site(self):
        with open('api/tests/example_ipstack_response.json') as json_file:
            example_data = json.loads(json_file.read())
            response_data = self.ip_handler.get_location_data('2606:4700:20::681a:754')
            self.assertEqual(example_data[1], response_data)

    def test_get_invalid_ipv6_site(self):
        response_data = self.ip_handler.get_location_data('260asd6:470asd0:20asd::681asda:65sad4')
        self.assertEqual(response_data, False)
