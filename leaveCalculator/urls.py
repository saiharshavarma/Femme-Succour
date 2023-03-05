from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.uploadPDF, name="uploadPDF"),
    path('dashboard', views.leavedash, name="leavedash"),
    path('profile/<slug:the_slug>', views.leaveprofile, name='leaveprofile'), 
]
