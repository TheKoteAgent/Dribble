from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView
from .google_auth import GoogleLogin

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]