from django.urls import path, include
from .views import SignUpView, LogInView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='api_sign_up'),
    path('log_in/', LogInView.as_view(), name='api_log_in'),
]
