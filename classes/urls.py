
from .views import Classroom_SearchAPI, CreateClassAPI

from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', CreateClassAPI.as_view(), name='create'),
    path('search/', Classroom_SearchAPI.as_view(), name='search'),

]