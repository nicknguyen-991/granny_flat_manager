from django.urls import path

from . import views

app_name = 'construction'

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/new/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path(
        'projects/<int:pk>/stages/<int:stage_pk>/',
        views.project_update_stage,
        name='project_update_stage',
    ),
    path('projects/<int:pk>/partners/', views.project_add_partner, name='project_add_partner'),
    path('projects/<int:pk>/updates/', views.project_add_update, name='project_add_update'),
]
