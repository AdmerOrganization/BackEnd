
from .views import CreateClassAPI

from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', CreateClassAPI.as_view(), name='create'),

]