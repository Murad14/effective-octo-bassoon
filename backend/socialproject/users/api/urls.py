from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    
)

from .views import RegisterAPIView, LogoutAPIView ,PasswordChangeAPIView, PasswordResetRequestAPIView, PasswordResetConfirmAPIView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
    
    path('register/', RegisterAPIView.as_view(), name='register_view'),
    path('logout/', LogoutAPIView.as_view(), name='logout_view'),
    path('password-change/', PasswordChangeAPIView.as_view(), name='password_change'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('reset-password/confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
]


