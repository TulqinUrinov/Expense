from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):

    def has_permission(self, request, view):
        return hasattr(request, 'user') and request.user is not None
