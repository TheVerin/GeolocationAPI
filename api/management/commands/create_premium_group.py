from django.core.management import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Creating Premium group...')
        Group.objects.create(name='Premium')
        self.stdout.write(self.style.SUCCESS('PremiumUser Group created'))
