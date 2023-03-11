from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user.is_staff
            or request.user.is_superuser
            or (request.user.groups.all())[0] == 'MANAGER'
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_staff
            or request.user.is_superuser
            or (request.user.groups.all())[0] == 'MANAGER'
        )
