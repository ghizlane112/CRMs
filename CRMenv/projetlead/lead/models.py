from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Lead(models.Model):
    STATUTS=[
      ('Nouveau','Nouveau'),
      ('Contacte','Contacte'),
      ('Qualifie','Qualifie'),
      ('Converti','Converti'),
      ('Perdu','Perdu')

    ]
    nom=models.CharField(max_length=20)
    prenom=models.CharField(max_length=20)
    email=models.EmailField()
    telephone=models.CharField(max_length=10)
    source=models.CharField(max_length=100)
    statut=models.CharField(max_length=50,choices=STATUTS)
    note=models.TextField(blank=True,null=True)
    date_creation=models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Interaction(models.Model):
    TYPE_CHOICES = [
        ('Appel', 'Appel'),
        ('SMS','SMS'),
        ('Email', 'Email'),
        ('Autre', 'Autre'),
    ]

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    lead = models.ForeignKey(Lead, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Interaction avec {self.lead} le {self.date}"








