from .views import SignUpAPI, SigninAPI
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', SignUpAPI.as_view(), name='signup'),
    path('signin/', SigninAPI.as_view(), name='signin'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]