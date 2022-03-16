
from .views import CurrentUserAPI, EditAPI, SignUpAPI, VerifyEmail, SigninAPI

from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='signup'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('signin/', SigninAPI.as_view(), name='signin'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('edit-profile/', EditAPI.as_view(), name='edit-profile'),
    path('user/', CurrentUserAPI.as_view()),
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password-reset')),
]