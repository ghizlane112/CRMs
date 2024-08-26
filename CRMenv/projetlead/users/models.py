from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 

class Member1User(AbstractUser):
    nom = models.CharField(max_length=15)
    prenom = models.CharField(max_length=15)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)  # Ajouté pour suivre la dernière activité

    # Ajoutez d'autres champs selon vos besoins

    # Redéfinir les relations pour éviter les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='member1user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='member1user_set',
        blank=True
    )
