from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    heur = models.TimeField()  # Champ pour l'heure de l'événement
    lieu=models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class History(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE,null=True, blank=True)
    action = models.CharField(max_length=50)  # e.g., 'delete'
    reason = models.TextField(blank=True, null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you use Django's User model
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title} -  le {self.timestamp}"

