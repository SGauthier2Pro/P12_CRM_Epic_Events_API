"""
serializer detail class for User model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.contrib.auth.models import User

from .userbaseserializer import UserBaseSerializer


class UserDetailSerializer(UserBaseSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'groups',
            'assigned_customers',
            'assigned_contracts',
            'assigned_events'
        ]
        read_only_fields = [
            'id',
            'username',
            'groups',
            'assigned_customers',
            'assigned_contracts',
            'assigned_events'
        ]
