from django.db import models

# Create your models here.


class CompanyPublicitaire(models.Model):
    name = models.CharField(max_length=255)  # Nom de l'entreprise
    address = models.TextField(null=True,blank=True)  # Adresse de l'entreprise
    contact_email = models.EmailField()  # Email de contact
    phone_number = models.CharField(max_length=20)  # Numéro de téléphone (optionnel)
   
    
    def __str__(self):
        return self.name
