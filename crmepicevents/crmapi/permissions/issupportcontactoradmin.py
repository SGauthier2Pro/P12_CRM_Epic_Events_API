from rest_framework import permissions


class IsSupportContactOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.all()[0] == 'SUPPORT':
            return True
        if request.user.is_superuser:
            return True
