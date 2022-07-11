from django.conf.urls import url
from requests import delete
from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static
from .views import ChatAPI, GetClassTokenAPI

"""
urlpatterns = [
    path('', chatAPI.as_view(), name='chat'),

]
"""
from . import views

urlpatterns = [
    path('<int:id>/', ChatAPI.as_view(), name='room'),
    path('class-token/<int:id>', GetClassTokenAPI.as_view(), name='getToken'),
]