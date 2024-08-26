from django.shortcuts import render

# Create your views here.
# notification/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    # Récupère les notifications pour l'utilisateur connecté
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()  # Compte les notifications non lues
    return render(request, 'notification/notifications.html', {'notifications': notifications,'unread_count': unread_count})



