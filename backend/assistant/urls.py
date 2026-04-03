from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),

    # Frontend-compatible endpoints
    path('upload/', views.upload_file, name='upload_file'),
    path('summary/', views.summary, name='summary'),

    # RESTful document API
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/summary/', views.document_summary, name='document_summary'),
    path('documents/<int:pk>/ask/', views.document_ask, name='document_ask'),
]