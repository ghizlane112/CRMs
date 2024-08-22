from django.db import models

# Create your models here.
# models.py

from django.contrib.auth.models import User

class Notification(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Pour les utilisateurs authentifiés
    lead_email = models.EmailField(null=True, blank=True)  # Pour les leads non authentifiés
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Pour marquer la notification comme lue

    #def _str_(self):
     #   return f'Notification pour {self.user if self.user else self.lead_email}'