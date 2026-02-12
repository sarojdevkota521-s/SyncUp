from django import forms
from tasks.models import Task
from projects.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()
class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["title", "project", "assigned_to"]

    def __init__(self, *args, **kwargs):
        workspace = kwargs.pop("workspace", None)
        super().__init__(*args, **kwargs)

        if workspace:
            self.fields["project"].queryset = Project.objects.filter(
                workspace=workspace
            )

            self.fields["assigned_to"].queryset = User.objects.filter(
                workspacemember__workspace=workspace
            )
