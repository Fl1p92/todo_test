from django.utils.decorators import method_decorator

from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


@method_decorator(name='list', decorator=swagger_auto_schema(
    manual_parameters=[
        Parameter('completed', IN_QUERY,
                  'Using for filter tasks by completed field. Example: `completed=true`',
                  type='bool')
    ],
))
class TaskViewSet(viewsets.ModelViewSet):
    """
    create:
    Create new task

    Create a new task for the current user.

    list:
    List of all tasks

    Returns information for all tasks of the current user.

    retrieve:
    Retrieve task

    Returns information for task of the current user.

    update:
    Update task

    Changes information for task of the current user.

    partial_update:
    Partial update task

    Changes partly information for task of the current user.

    destroy:
    Destroy task

    Delete the task of the current user.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer
    filterset_fields = ['completed']

    def get_queryset(self):
        queryset = Task.objects.all()

        # A little trick to fix an exception that occurs during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return queryset

        # Filter by request user
        queryset = queryset.filter(user=self.request.user)
        return queryset
