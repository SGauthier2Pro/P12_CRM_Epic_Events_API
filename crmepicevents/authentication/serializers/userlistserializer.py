"""
serializer class for User model
@create : function for adding author id at creation
@author : Sylvain GAUTHIER
@version : 1.0
"""

from django.contrib.auth.models import User

from .userbaseserializer import UserBaseSerializer


class UserListSerializer(UserBaseSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'groups'
        ]
        read_only_fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'groups'
        ]
