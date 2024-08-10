from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet
from . import views

router = DefaultRouter()
router.register('events', EventViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('calendar/',views.calendar, name='calendar'),
     path('events/', views.event_list, name='event-list'),
   # path('calendar/',TemplateView.as_view(template_name="appoitementfile/calendar.html"), name='calendar'),
]