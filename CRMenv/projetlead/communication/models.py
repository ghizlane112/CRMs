from django.db import models
from lead.models import Lead
from django.conf import settings


# Create your models here.
class Message(models.Model):
   # sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
   # receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
   # sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    #receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Message from {self.sender} to {self.receiver} on {self.timestamp}"