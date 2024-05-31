from django.urls import path
from . import views

urlpatterns = [
    path('', views.uploadfile, name='uploadfile'),
    path('format_uploaded_file/', views.formatfile,name='format_uploaded_file' ),
]
