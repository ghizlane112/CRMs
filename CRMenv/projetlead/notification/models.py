from django.db import models
from django.contrib.auth.models import User
from Rendez.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    RECIPIENT_TYPE_CHOICES = [
        ('user', 'Utilisateur')
    ]

    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_TYPE_CHOICES, default='user')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)  # Ajoutez ce champ
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def _str_(self):
        return f"Notification for {self.recipient_user.username} about event {self.event}"

    class Meta:
        ordering = ['-created_at']



        
class Reminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    note = models.TextField()
    is_sent = models.BooleanField(default=False)  # Ajoutez ce champ

    def __str__(self):
        return f"Rappel pour {self.event.title} le {self.reminder_time}"