from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from projects.models import Project
from tasks.models import Task
from django.http import HttpResponseForbidden
from workspaces.models import WorkspaceMember

from .forms import TaskForm , WorkspaceMemberForm
from .models import Workspace

# Create your views here.


def home(request):

    membership = WorkspaceMember.objects.filter(
        user=request.user
    ).first()

    if membership:
        return redirect(
            "workspace-dashboard",
            workspace_slug=membership.workspace.slug
        )

    workspace = request.workspace 
    # Workspace.objects.filter(owner=request.user)

    if request.method == "POST":
        form = WorkspaceMemberForm(request.POST)

        if form.is_valid():
            member = form.save(commit=False)
            member.workspace = workspace
            member.user = request.user
            member.save()

            return redirect(
                "workspace-dashboard",
                workspace_slug=workspace.slug
            )
    else:
        form = WorkspaceMemberForm()

    return render(request, "home.html", {
        "workspace": workspace,
        "form": form
    })
@login_required
def workspace_dashboard(request, workspace_slug):
    workspace = request.workspace

    projects = Project.objects.filter(workspace=workspace)
    tasks = Task.objects.for_workspace(workspace)
    is_owner = workspace.owner == request.user

    context = {
        "workspace": workspace,
        "projects": projects,
        "tasks": tasks,
        "is_owner":is_owner
    }

    return render(request, "workspaces/dashboard.html", context)

@login_required
def project_list(request, workspace_slug):
    workspace = request.workspace

    projects = Project.objects.filter(workspace=workspace)

    return render(
        request,
        "projects/project_list.html",
        {
            "workspace": workspace,
            "projects": projects
        }
    )


def check_workspace_membership(user, workspace):
    return WorkspaceMember.objects.filter(
        user=user,
        workspace=workspace
    ).exists()
from projects.forms import ProjectForm
@login_required
def project_create(request, workspace_slug):
    workspace = request.workspace

    if request.method == "POST":
        form = ProjectForm(request.POST, workspace=workspace)
        if form.is_valid():
            task = form.save(commit=False)
            task.workspace = workspace
            
            task.save()
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
    workspace = request.workspace

    if not check_workspace_membership(request.user, workspace):
        return HttpResponseForbidden("Access denied")

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
    workspace = request.workspace

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
    workspace = request.workspace

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
