from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase


class CommandTest(TestCase):

    def test_create_premium_group(self):
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            call_command('create_premium_group')
            self.assertEqual(gi.call_count, 1)
