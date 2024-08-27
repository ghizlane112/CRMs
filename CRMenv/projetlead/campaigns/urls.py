from django.urls import path
from . import views

urlpatterns = [
    path('campaigns/', views.campaign_list, name='campaign_list'),
]
