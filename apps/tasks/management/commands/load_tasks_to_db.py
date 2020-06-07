import requests

from django.core.management.base import BaseCommand

from apps.tasks.serializers import TaskSerializer


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
        with requests.Session() as session:
            data = session.get(self.server_url)
            response_data = data.json()
        self.stdout.write(self.style.MIGRATE_HEADING(f'Parsed {len(response_data)} objects.'))

        # Deserialize data into objects
        tasks = []
        for task_data in response_data:
            task_data['user'] = task_data.pop('userId')
            serializer = TaskSerializer(data=task_data)
            if serializer.is_valid():
                task = serializer.save()
                tasks.append(task)

        self.stdout.write(self.style.SUCCESS(f"Created new {len(tasks)} user's tasks."))
