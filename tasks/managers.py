from django.db import models

class TaskQuerySet(models.QuerySet):
    def for_workspace(self, workspace):
        return self.filter(workspace=workspace)

class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def for_workspace(self, workspace):
        return self.get_queryset().for_workspace(workspace)
