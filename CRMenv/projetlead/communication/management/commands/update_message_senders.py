# myapp/management/commands/update_message_senders.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from communication.models import Message

User = get_user_model()

class Command(BaseCommand):
    help = 'Update sender field for all messages'

    def handle(self, *args, **kwargs):
        # Assurez-vous d'avoir un utilisateur par défaut à utiliser pour les mises à jour
        default_user = User.objects.first()  # Vous pouvez changer cela pour un utilisateur spécifique si nécessaire
        
        if not default_user:
            self.stdout.write(self.style.ERROR('No default user found.'))
            return

        # Mettez à jour les messages sans sender
        messages_updated = Message.objects.filter(sender__isnull=True).update(sender=default_user)
        self.stdout.write(self.style.SUCCESS(f'Updated {messages_updated} messages with default sender.'))