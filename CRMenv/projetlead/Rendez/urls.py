from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar_view'),  # La vue principale pour /event
    path('events/', views.event_list, name='event_list'), 
    path('add-event/', views.add_event, name='add_event'),
    path('update-event/', views.update_event, name='update_event'),
    path('delete-event/', views.delete_event, name='delete_event'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'), # L'URL pour obtenir les événements
]
