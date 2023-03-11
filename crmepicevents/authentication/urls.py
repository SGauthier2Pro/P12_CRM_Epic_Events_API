from django.urls import path, include
from .views.myobtaintokenpairview import MyObtainTokenPairView
from .views.userviewset import UserViewSet

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('users',
                UserViewSet,
                basename='users')

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]