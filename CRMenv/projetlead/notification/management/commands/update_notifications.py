# notification/management/commands/update_notifications.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notification.models import Notification

User = get_user_model()

class Command(BaseCommand):
    help = 'Met à jour les notifications existantes pour définir un destinataire par défaut'

    def handle(self, *args, **options):
        default_user = User.objects.first()  # Choisissez un utilisateur par défaut ou un utilisateur valide
        
        if not default_user:
            self.stdout.write(self.style.ERROR('Aucun utilisateur trouvé pour définir comme destinataire par défaut.'))
            return

        notifications = Notification.objects.filter(recipient__isnull=True)
        count = notifications.update(recipient=default_user)

        self.stdout.write(self.style.SUCCESS(f'Updated {count} notifications with default recipient.'))