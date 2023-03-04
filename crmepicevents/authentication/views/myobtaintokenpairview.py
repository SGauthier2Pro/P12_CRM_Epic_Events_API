"""
view class managing token access distribution for users

@author : Sylvain GAUTHIER
@version : 1.0
"""


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from ..serializers.mytokenobtainpairserializer import \
    MyTokenObtainPairSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MyTokenObtainPairSerializer
