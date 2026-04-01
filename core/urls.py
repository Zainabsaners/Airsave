from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserView, LoginView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]