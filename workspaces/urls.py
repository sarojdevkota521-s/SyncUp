from django.urls import path
from . import views

urlpatterns = [
    
    # path("", views.home, name="home"),

    path("<slug:workspace_slug>/", views.workspace_dashboard, name="workspace-dashboard"),
    path("<slug:workspace_slug>/projects/", views.project_list, name="project-list"),
    path("<slug:workspace_slug>/projects/create/", views.project_create, name="project-create"),
    path("<slug:workspace_slug>/tasks/", views.task_list, name="task-list"),
    path("<slug:workspace_slug>/tasks/create/", views.task_create, name="task-create"),
    path("<slug:workspace_slug>/tasks/<int:pk>/", views.task_detail, name="task-detail"),
]
