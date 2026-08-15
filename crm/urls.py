from django.urls import path

from . import views

app_name = 'crm'

urlpatterns = [
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/pipeline/', views.lead_pipeline, name='lead_pipeline'),
    path('leads/new/', views.lead_create, name='lead_create'),
    path('leads/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('leads/<int:pk>/edit/', views.lead_edit, name='lead_edit'),
    path('leads/<int:pk>/status/', views.lead_update_status, name='lead_update_status'),
    path('leads/<int:pk>/convert/', views.lead_convert_to_client, name='lead_convert'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/new/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/edit/', views.client_edit, name='client_edit'),
]
