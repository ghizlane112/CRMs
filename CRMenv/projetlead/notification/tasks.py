from celery import shared_task
from django.utils import timezone
from Rendez.models import Event  # Assurez-vous que le chemin est correct
from .models import Notification

@shared_task
def create_event_reminders():
    """Créer des rappels pour les événements pour les utilisateurs."""
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gt=today)  # Filtrer les événements futurs

    for event in upcoming_events:
        reminder_date = event.date - timezone.timedelta(days=1)
        if reminder_date == today:
            # Créer une notification pour l'utilisateur concerné
            Notification.objects.create(
                recipient_user=event.user,  # Assurez-vous que 'user' est bien défini dans votre modèle Event
                event=event,
                message=f'Rappel : Vous avez un événement avec {event.lead.nom} prévu pour le {event.date} à {event.time}.',
                recipient_type='user'  # 'user' est défini dans les options du modèle Notification
            )