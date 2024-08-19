from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),  # La vue principale pour /event
    path('events/', views.event_list, name='event_list'),  # L'URL pour obtenir les événements
]
