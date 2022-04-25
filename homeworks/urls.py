from msilib.schema import CreateFolder
from django.conf.urls import url
from requests import delete
from .views import CreateHomeworkAPI 
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', CreateHomeworkAPI.as_view(), name='createHomework'),

]
