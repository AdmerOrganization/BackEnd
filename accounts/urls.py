from .views import SignUpAPI, VerifyEmail
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='signup'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]