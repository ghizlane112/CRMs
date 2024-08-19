from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    heur = models.TimeField()  # Champ pour l'heure de l'événement
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
