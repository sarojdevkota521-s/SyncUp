from django.utils.deprecation import MiddlewareMixin
from workspaces.models import Workspace

class WorkspaceMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        request.workspace = None

        if request.user.is_authenticated:
            slug = view_kwargs.get("workspace_slug")

            if slug:
                try:
                    request.workspace = Workspace.objects.get(slug=slug)
                except Workspace.DoesNotExist:
                    request.workspace = None
