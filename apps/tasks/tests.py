from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.factories import UserFactory, USER_TESTING_PASSWORD
from .factories import TaskFactory
from .models import Task


class TaskAPIViewTest(APITestCase):
    """
    Test cases for tasks API endpoints.
    """

    def setUp(self):
        self.count = 10
        # Create 10 tasks for random users
        for _ in range(self.count):
            TaskFactory()
        self.test_user = UserFactory()
        # Create 19 tasks for test user
        for _ in range(self.count * 2 - 1):
            TaskFactory(user=self.test_user)
        # Create 1 more testing task for test user
        self.test_task = TaskFactory(user=self.test_user)
        self.list_create_url = reverse('todo-list')
        self.access_token = self.get_access_token()

    def get_access_token(self):
        response = self.client.post(reverse('token_obtain_pair'),
                                    data={'username': self.test_user.username,
                                          'password': USER_TESTING_PASSWORD},
                                    format='json')
        return response.data['access']

    def test_tasks_list(self):
        # unauthorized request
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        # all tasks
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.count * 2)  # 20 for test user
        self.assertEqual(Task.objects.count(), self.count * 3)  # 30 for all users (include test user)

        # filtered by completed=true
        response = self.client.get(self.list_create_url, data={'completed': 'true'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.filter(user=self.test_user, completed=True).count())

    def test_task_create(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        data = {'title': 'New test todo', 'completed': True}
        self.assertEqual(Task.objects.count(), self.count * 3)

        response = self.client.post(self.list_create_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), self.count * 3 + 1)  # 30 + 1
        self.assertEqual(Task.objects.filter(user=self.test_user).count(), self.count * 2 + 1)  # 20 + 1
        self.assertEqual(
            Task.objects.filter(user=self.test_user).values_list('title', 'completed').last(),
            (data['title'], data['completed'])
        )

    def test_task_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        response = self.client.get(reverse('todo-detail', kwargs={'pk': self.test_task.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.test_user.id)
        self.assertEqual(response.data['title'], self.test_task.title)
        self.assertEqual(response.data['completed'], self.test_task.completed)

        # bad task id
        last_id = Task.objects.values_list('id', flat=True).last()
        response = self.client.get(reverse('todo-detail', kwargs={'pk': last_id + 100500}), format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_update(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # test mass update via put
        put_data = {'title': 'New title test1', 'completed': False}
        response = self.client.put(reverse('todo-detail', kwargs={'pk': self.test_task.id}),
                                   data=put_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.title, put_data['title'])
        self.assertEqual(self.test_task.completed, put_data['completed'])

        # test partial update via patch
        patch_data = {'completed': True}
        response = self.client.patch(reverse('todo-detail', kwargs={'pk': self.test_task.id}),
                                     data=patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.completed, patch_data['completed'])

    def test_task_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(Task.objects.count(), self.count * 3)  # 30 tasks

        response = self.client.delete(reverse('todo-detail', kwargs={'pk': self.test_task.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), self.count * 3 - 1)  # 29 tasks
        self.assertEqual(Task.objects.filter(user=self.test_user).count(), self.count * 2 - 1)  # 19 tasks for our user
