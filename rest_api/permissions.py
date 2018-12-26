from rest_framework.permissions import BasePermission

from rest_api.models.User import Role


class IsAdminRole(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user.has_admin_role()
