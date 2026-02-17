from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from projects.models import Project
from tasks.models import Task
from django.http import HttpResponseForbidden
from workspaces.models import WorkspaceMember, Workspace
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.text import slugify

from .forms import TaskForm , WorkspaceMemberForm
from .models import Workspace


from django.core.exceptions import PermissionDenied
def get_workspace_for_user(user, workspace_slug):
    return get_object_or_404(
        Workspace,
        slug=workspace_slug,
        members=user,
    )
@login_required
def workspace_dashboard(request, workspace_slug):
    workspace = get_workspace_for_user(request.user, workspace_slug)

    projects = Project.objects.filter(workspace=workspace)
    tasks = Task.objects.for_workspace(workspace)
    
    
        
    context = {
        "workspace": workspace,
        "projects": projects,
        "tasks": tasks,
        
    }

    return render(request, "workspaces/dashboard.html", context)

@login_required
def project_list(request, workspace_slug):
    workspace = get_workspace_for_user(request.user, workspace_slug)
    projects = Project.objects.filter(workspace=workspace)

    return render(
        request,
        "projects/project_list.html",
        {
            "workspace": workspace,
            "projects": projects,
        },
    )
from projects.forms import ProjectForm
@login_required
def project_create(request, workspace_slug):
    workspace = get_workspace_for_user(request.user, workspace_slug)

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.workspace = workspace
            project.save()
            return redirect("project-list", workspace_slug=workspace.slug)
    else:
        form = ProjectForm()

    return render(
        request,
        "projects/project_form.html",
        {
            "workspace": workspace,
            "form": form
        }
    )


@login_required
def task_list(request, workspace_slug):
    workspace = get_workspace_for_user(request.user, workspace_slug)

    tasks = Task.objects.for_workspace(workspace)

    return render(
        request,
        "tasks/task_list.html",
        {
            "workspace": workspace,
            "tasks": tasks
        }
    )

from django.shortcuts import get_object_or_404

@login_required
def task_detail(request, workspace_slug, pk):
    workspace = get_workspace_for_user(request.user, workspace_slug)
    task = get_object_or_404(
        Task,
        id=pk,
        workspace=workspace 
    )

    return render(
        request,
        "tasks/task_details.html",
        {
            "workspace": workspace,
            "task": task
        }
    )



@login_required
def task_create(request, workspace_slug):
    workspace = get_workspace_for_user(request.user, workspace_slug)
    if request.method == "POST":
        form = TaskForm(request.POST, workspace=workspace)
        if form.is_valid():
            task = form.save(commit=False)
            task.workspace = workspace
            task.save()
            return redirect("task-list", workspace_slug=workspace.slug)
    else:
        form = TaskForm(workspace=workspace)

    return render(
        request,
        "tasks/task_form.html",
        {
            "workspace": workspace,
            "form": form
        }
    )
