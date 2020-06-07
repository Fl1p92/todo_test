from django.db import models


class Task(models.Model):
    """
    User's task representation.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100, blank=True, default='')
    completed = models.BooleanField(default=False, help_text='Indicates completion of the task.')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.user}'s task [{self.id}]"
