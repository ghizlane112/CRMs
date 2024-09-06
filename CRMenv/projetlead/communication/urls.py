from django.urls import path
from .views import inbox
from lead import views

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
   # path('send_message/', send_message, name='send_message'),
      path('dashboard/',views.dashboard,name='dashboard'),
]