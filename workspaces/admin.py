from django.contrib import admin
from .models import Workspace,WorkspaceMember

# Register your models here.
admin.site.register(Workspace)
admin.site.register(WorkspaceMember)