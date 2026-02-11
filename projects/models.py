from django.db import models
from workspaces.models import Workspace

class Project(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)