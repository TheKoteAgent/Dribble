from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from .views import RegisterView, UserProfileView
from .google_auth import GoogleLogin

urlpatterns = [
    # Аутентифікація
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/', GoogleLogin.as_view(), name='google_login'),

    # Відновлення пароля (лист із посиланням uid+token на фронтенд)
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),

    # Приватний профіль
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]