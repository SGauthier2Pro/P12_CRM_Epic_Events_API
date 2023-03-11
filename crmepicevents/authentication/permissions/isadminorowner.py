from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        if request.user.is_superuser:
            return True
