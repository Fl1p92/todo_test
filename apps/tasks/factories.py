import factory

from apps.users.factories import UserFactory
from .models import Task


class TaskFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f'test task{n}')
    completed = factory.Iterator([True, False])

    class Meta:
        model = Task
