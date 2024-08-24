from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_view, name='report_dashboard'),
    path('reports/<int:report_id>/', views.report_view, name='report_detail'),
]