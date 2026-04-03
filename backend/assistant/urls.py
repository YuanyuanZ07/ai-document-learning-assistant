from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('upload/', views.upload_file, name='upload_file'),
    path('summary/', views.summary, name='summary'),
]