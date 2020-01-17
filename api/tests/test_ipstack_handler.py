import json

from django.test import TestCase

from api.tools.ipstack_handling import IPStackHandler


class ExternalApiTest(TestCase):

    def setUp(self) -> None:
        self.ip_handler = IPStackHandler()

    def test_ipv4_site(self):
        self.assertEqual(self.ip_handler.payload_validation('1.1.1.1'), '1.1.1.1')

    def test_ipv6_site(self):
        self.assertEqual(self.ip_handler.payload_validation('2606:4700:20::681a:754'),
                         '2606:4700:20::681a:754')

    def test_www_url_site(self):
        self.assertEqual(self.ip_handler.payload_validation('www.sofomo.com'), 'www.sofomo.com')

    def test_url_site(self):
        self.assertEqual(self.ip_handler.payload_validation('sofomo.com'), 'sofomo.com')

    def test_https_url_site(self):
        self.assertEqual(self.ip_handler.payload_validation('https://sofomo.com'), 'sofomo.com')

    def test_https_www_url_site(self):
        self.assertEqual(self.ip_handler.payload_validation('https://www.sofomo.com'),
                         'www.sofomo.com')

    def test_http_url_site(self):
        self.assertEqual(self.ip_handler.payload_validation('http://sofomo.com'), 'sofomo.com')

    def test_http_www_url_site(self):
        self.assertEqual(self.ip_handler.payload_validation('http://www.sofomo.com'),
                         'www.sofomo.com')

    def test_get_valid_ipv4_site(self):
        with open('api/tests/example_ipstack_response.json') as json_file:
            example_data = json.loads(json_file.read())
            response_data = self.ip_handler.get_location_data('176.32.103.205')
            self.assertEqual(example_data[0], response_data)

    def test_get_invalid_ipv4_site(self):
        self.assertRaises(ValueError, self.ip_handler.get_location_data, '1111.1111.1111.1111')

    def test_get_invalid_url_site(self):
        self.assertRaises(ValueError, self.ip_handler.get_location_data,
                          'ibetthereisnowebsitelikethis.com')

    def test_get_valid_ipv6_site(self):
        with open('api/tests/example_ipstack_response.json') as json_file:
            example_data = json.loads(json_file.read())
            response_data = self.ip_handler.get_location_data('2606:4700:20::681a:754')
            self.assertEqual(example_data[1], response_data)

    def test_get_invalid_ipv6_site(self):
        self.assertRaises(ValueError, self.ip_handler.get_location_data,
                          '260asd6:470asd0:20asd::681asda:65sad4')

    def test_to_much_input_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data,
                          '260asd6:470asd0:20asd::681asda:65sad4', 'second')

    def test_no_input_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data)

    def test_int_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data, 22)

    def test_float_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data, 22.99)

    def test_bool_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data, True)

    def test_list_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data, [12, 34])

    def test_tuple_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data, (12, 34))

    def test_set_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data, {12, 34})

    def test_dict_data(self):
        self.assertRaises(TypeError, self.ip_handler.get_location_data, {'a': 12, 'b': 34})
