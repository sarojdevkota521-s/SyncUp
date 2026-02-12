from django import forms
from tasks.models import Task
from projects.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = '__all__'