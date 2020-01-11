from api.tools.payload_validation import PayloadValidator

from django.test import TestCase


class PayloadValidatorTest(TestCase):

    def setUp(self) -> None:
        self.validator = PayloadValidator()

    def test_ipv4_site(self):
        self.assertEqual(self.validator.payload_validation('1.1.1.1'), ['1.1.1.1', 'ip'])

    def test_ipv6_site(self):
        self.assertEqual(self.validator.payload_validation('2606:4700:20::681a:754'),
                         ['2606:4700:20::681a:754', 'ip'])

    def test_www_url_site(self):
        self.assertEqual(self.validator.payload_validation('www.sofomo.com'),
                         ['www.sofomo.com', 'url'])

    def test_url_site(self):
        self.assertEqual(self.validator.payload_validation('sofomo.com'),
                         ['sofomo.com', 'url'])

    def test_https_url_site(self):
        self.assertEqual(self.validator.payload_validation('https://sofomo.com'),
                         ['sofomo.com', 'url'])

    def test_https_www_url_site(self):
        self.assertEqual(self.validator.payload_validation('https://www.sofomo.com'),
                         ['www.sofomo.com', 'url'])

    def test_http_url_site(self):
        self.assertEqual(self.validator.payload_validation('http://sofomo.com'),
                         ['sofomo.com', 'url'])

    def test_http_www_url_site(self):
        self.assertEqual(self.validator.payload_validation('http://www.sofomo.com'),
                         ['www.sofomo.com', 'url'])
