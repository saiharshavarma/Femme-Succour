from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.uploadVideo, name="uploadVideo"),
]
