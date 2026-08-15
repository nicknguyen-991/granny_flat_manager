from django.urls import path

from . import views

app_name = 'reporting'

urlpatterns = [
    path('reports/', views.dashboard, name='dashboard'),
]
