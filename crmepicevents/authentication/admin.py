from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(UserAdmin):
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)


UserAdmin.list_display = (
    'username',
    'first_name',
    'last_name',
    'email',
    'is_active',
    'is_staff',
    'is_superuser',
    'date_joined',
    'last_login',
    'group'
)

