from django.urls import path
from . import views
from .views import LeadListCreate, LeadDetail

urlpatterns = [
    path('', views.one, name='one'),

    path('two',views.two,name='two'),
    path('three',views.three,name='three'),
    path('dashboard',views.four,name='dashboard'),
    path('leadlist', views.lead_list, name='lead_list'),
    path('lead/<int:pk>/', views.lead_detail, name='lead_detail'),
    path('lead/new/', views.lead_create, name='lead_create'),
    path('lead/import/', views.lead_import, name='lead_import'),
   

   path('api/leads/', LeadListCreate.as_view(), name='lead-list-create'),
    path('api/leads/<int:pk>/', LeadDetail.as_view(), name='lead-detail'),
    ]