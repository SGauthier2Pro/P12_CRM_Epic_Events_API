from rest_framework import permissions


class IsSalesContactOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if str(request.user.groups.all()[0]) == 'SALES':
            return True
        if request.user.is_superuser:
            return True
