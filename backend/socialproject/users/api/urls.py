from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)

from .views import RegisterAPIView


urlpatterns = [
    #path ('', views.getRoutes),
    path('login/', TokenObtainPairView.as_view(), name='login_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    
    path('register/', RegisterAPIView.as_view(), name='register_view'),
    
]


