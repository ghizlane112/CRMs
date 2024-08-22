from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import SomeModel  # Remplacez 'myapp' et 'SomeModel' par votre application et modèle

class Command(BaseCommand):
    help = 'Créer des groupes et attribuer des permissions'

    def handle(self, *args, **kwargs):
        # Créer un groupe pour les administrateurs
        admin_group, created = Group.objects.get_or_create(name='Administrateurs')

        # Créer un groupe pour les utilisateurs normaux
        user_group, created = Group.objects.get_or_create(name='Utilisateurs')

        # Attribuer des permissions au groupe administrateurs
        content_type = ContentType.objects.get_for_model(SomeModel)
        permissions = Permission.objects.filter(content_type=content_type)
        admin_group.permissions.set(permissions)

        # Attribuer des permissions spécifiques aux utilisateurs normaux
        user_permissions = Permission.objects.filter(content_type=content_type, codename__in=['view_somemodel'])
        user_group.permissions.set(user_permissions)

        self.stdout.write(self.style.SUCCESS('Groupes et permissions créés avec succès'))