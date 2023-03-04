"""
view class managing the registering for new user

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from ..serializers.registerserializer import RegisterSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser,)
    serializer_class = RegisterSerializer
