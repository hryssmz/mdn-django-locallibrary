# catalog/urls.py
from django.urls import path

from . import apis, views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/", apis.index_api, name="index-api"),
]
