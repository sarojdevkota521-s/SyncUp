from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import RegisterForm
from workspaces.models import Workspace
from django.utils.text import slugify

# Create your views here.
def _build_unique_workspace_slug(username):
    base_slug = slugify(username) or "workspace"
    slug = base_slug
    suffix = 1

    while Workspace.objects.filter(slug=slug).exists():
        suffix += 1
        slug = f"{base_slug}-{suffix}"

    return slug

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            workspace = Workspace.objects.create(
                 name=f"{user.username}'s Workspace",
                slug=_build_unique_workspace_slug(user.username),
                owner=user,
            )

            workspace.members.add(user)

            return redirect("workspace-dashboard", workspace_slug=workspace.slug)
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})
def login_view(request):
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            workspace = Workspace.objects.filter(members=user).order_by("id").first()
            if workspace:
                return redirect("workspace-dashboard", workspace_slug=workspace.slug)
            return redirect("logout")

    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")