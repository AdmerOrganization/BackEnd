from django.conf.urls import url
from requests import delete
from .views import Classroom_SearchAPI, CreateClassAPI, ListClasses, ListClassesById,\
    DeleteClassesAPI, EditEventsAPI, ListCreatedClasses
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', CreateClassAPI.as_view(), name='create'),
    path('search/', Classroom_SearchAPI.as_view(), name='search'),
    path('get-all/', ListClasses.as_view(), name='get all'),
    url(r'^get-id/(?P<pk>[0-9]+)/$',
        ListClassesById.as_view(), name='list-class-by-id'),
    path('get-created/', ListCreatedClasses.as_view(), name='get created'),
    path('delete/', DeleteClassesAPI.as_view(), name='delete'),
    path('edit/', EditEventsAPI.as_view(), name='edit'),
]
