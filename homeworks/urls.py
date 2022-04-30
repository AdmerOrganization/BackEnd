from msilib.schema import CreateFolder
from django.conf.urls import url
from requests import delete
from .views import CreateHomeworkAPI, DisplayHomeworkAPI, EditHomeworkAPI,ListHomeworkAPI
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', CreateHomeworkAPI.as_view(), name='createHomework'),
    path('edit/', EditHomeworkAPI.as_view(), name='editHomework'),
    path('display/', DisplayHomeworkAPI.as_view(), name='displayHomework'),
    path('list/', ListHomeworkAPI.as_view(), name='listHomework'),
]
