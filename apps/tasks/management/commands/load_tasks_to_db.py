import requests

from django.core.management.base import BaseCommand
from django.http import HttpRequest

from apps.tasks.serializers import TaskSerializer
from apps.users.models import User


class Command(BaseCommand):
    """
    This command is intended for initial database loading.
    When you call again, it will fill the database with duplicate tasks.
    """
    server_url = 'https://jsonplaceholder.typicode.com/todos'
    help = f"""Loads tasks info to the db from the {server_url}.
              Example: docker exec -it backend python manage.py load_tasks_to_db"""

    def handle(self, *args, **options):
        # Get data from site
        data = requests.get(self.server_url)
        response_data = data.json()
        self.stdout.write(self.style.MIGRATE_HEADING(f'Parsed {len(response_data)} objects.'))

        # Deserialize data into objects
        tasks = []
        for task_data in response_data:
            user = User.objects.filter(id=task_data.pop('userId')).first()
            if user is not None:
                # request object with user is obligated in TaskSerializer
                request = HttpRequest()
                request.user = user
                serializer = TaskSerializer(data=task_data, context={'request': request})
                if serializer.is_valid():
                    task = serializer.save()
                    tasks.append(task)

        self.stdout.write(self.style.SUCCESS(f"Created new {len(tasks)} user's tasks."))
