from django.db import models
from workspaces.models import Workspace
from projects.models import Project
from django.conf import settings
from .managers import TaskManager
# Create your models here.
class Task(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    objects = TaskManager()

    def __str__(self):
        return self.title