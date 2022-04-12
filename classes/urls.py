from django.conf.urls import url
from .views import Classroom_SearchAPI, CreateClassAPI, ListClasses, ListClassesById

from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', CreateClassAPI.as_view(), name='create'),
    path('search/', Classroom_SearchAPI.as_view(), name='search'),
    path('get-all/', ListClasses.as_view(), name='get all'),
    url(r'^get-id/(?P<pk>[0-9]+)/$', ListClassesById.as_view(), name='list-class-by-id')
]