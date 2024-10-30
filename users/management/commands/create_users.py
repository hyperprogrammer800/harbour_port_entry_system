from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create multiple users'

    def handle(self, *args, **options):
        for i in range(0, 100):
            username = f'user{i}'
            password = 'Test@1234'
            email = f'user0{i}@example.com'

            user = User.objects.create_user(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Created user: {username} with password: {password}'))
