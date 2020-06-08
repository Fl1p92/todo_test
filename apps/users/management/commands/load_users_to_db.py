import requests

from django.core.management.base import BaseCommand

from apps.users.models import User
from apps.users.serializers import UserSerializer


class Command(BaseCommand):
    """
    This command is intended for initial database loading.
    When you call again, nothing will happen, because the username is not unique.
    """
    test_password = 'VerySecurityPassword123'
    server_url = 'https://jsonplaceholder.typicode.com/users'
    help = f"""Loads users info to the db from the {server_url}.
              Example: docker exec -it backend python manage.py load_users_to_db"""

    def handle(self, *args, **options):
        # Get data from site
        data = requests.get(self.server_url)
        response_data = data.json()
        self.stdout.write(self.style.MIGRATE_HEADING(f'Parsed {len(response_data)} objects.'))

        # Deserialize data into objects
        users = []
        for user_data in response_data:
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(self.test_password)
                users.append(user)

        # Add password for created users
        User.objects.bulk_update(users, ['password'])
        if users:
            self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users with passwords and additional data.'))
