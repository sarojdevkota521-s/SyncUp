from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import RegisterForm
from workspaces.models import Workspace
from django.utils.text import slugify

# Create your views here.

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            workspace_name = f"{user.username}'s Workspace"
            workspace_slug = slugify(user.username)

            workspace = Workspace.objects.create(
                name=workspace_name,
                slug=workspace_slug,
                owner=user,
            )

            workspace.members.add(user)

            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})
def login_view(request):
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            workspace = Workspace.objects.filter(
                owner=request.user
            ).first()
           
            
            return redirect(
                    "workspace-dashboard",
                    workspace_slug=workspace.slug
                )
            

    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")