from django.db import models

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


    def __str__(self):
        return f"{self.prenom} {self.nom}"







