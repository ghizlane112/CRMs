from django.shortcuts import render

# Create your views here.
# notification/views.py
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.utils import timezone
from datetime import timedelta
from .models import Reminder, Event
from .forms import ReminderForm
from django.http import JsonResponse




@login_required
def notifications(request):
    if request.method == 'POST':
        # Marquer les notifications comme lues
        notification_ids = request.POST.getlist('notification_ids[]')
        Notification.objects.filter(id__in=notification_ids, recipient=request.user).update(is_read=True)
        return JsonResponse({'status': 'success'})

    # GET request handling
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retourne les données en JSON pour les appels AJAX
        notifications_data = list(notifications.values('id', 'sender', 'message', 'created_at', 'is_read'))
        return JsonResponse({'unread_count': unread_count, 'notifications': notifications_data})

    return render(request, 'notification/notifications.html', {'notifications': notifications, 'unread_count': unread_count})


@login_required
def list_reminders(request):
    reminders = Reminder.objects.filter(user=request.user)  # Filtre les rappels pour l'utilisateur connecté
    return render(request, 'notification/list_reminders.html', {'reminders': reminders})



@login_required
def create_reminder(request, event_id=None):
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    else:
        event = None

    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.event = event
            reminder.save()
            
            # Créer une notification immédiatement pour le rappel
            Notification.objects.create(
                recipient=request.user,
                sender=None,  # Vous pouvez définir un utilisateur spécifique si nécessaire
                message=f"Rappel: {reminder.note} à {reminder.reminder_time}",
                is_read=False
            )
            
            return redirect('calendar')
    else:
        form = ReminderForm()

    return render(request, 'notification/create_reminder.html', {'form': form, 'event': event})



def viewD(request):
    user = request.user
    notifications = Notification.objects.filter(recipient=user, is_read=False).order_by('-timestamp')
    
    # Marquer les notifications comme lues après affichage
    notifications.update(is_read=True)
    
    return render(request, 'notification/notifications.html', {'notifications': notifications})





def check_reminders():
    now = timezone.now()
    reminders = Reminder.objects.filter(reminder_time__lte=now, is_sent=False)
    for reminder in reminders:
        # Créer une notification pour le rappel
        Notification.objects.create(
            recipient=reminder.user,
            sender=None,  # Vous pouvez définir un utilisateur spécifique si nécessaire
            message=f"Rappel: {reminder.note}",
            is_read=False
        )
        reminder.is_sent = True
        reminder.save()