"""
serializer admin class for User model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.contrib.auth.models import User

from .userbaseserializer import UserBaseSerializer


class UserAdminSerializer(UserBaseSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
            'password',
            'groups',
            'assigned_customers',
            'assigned_contracts',
            'assigned_events'
        ]