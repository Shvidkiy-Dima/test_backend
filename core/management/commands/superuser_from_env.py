from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import os


class Command(BaseCommand):

    def handle(self,  **options):
        name = os.environ.get('SUPERUSER_NAME', 'admin')
        password = os.environ.get('SUPERUSER_PASSWORD', 'admin')
        User = get_user_model()
        if not User.objects.filter(username=name).exists():
            User.objects.create_superuser(username=name, password=password)
            self.stdout.write('SUPERUSER WAS CREATED!')
        else:
            self.stderr.write('SUPERUSER ALREADY EXISTS!')
