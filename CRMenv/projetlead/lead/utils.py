from users.models import Member1User
from .models import Lead

def affectation_automatique(lead):
    # Trouver tous les utilisateurs
    utilisateurs = Member1User.objects.all()
    # Trouver l'utilisateur avec le moins de leads en cours
    utilisateur_disponible = min(utilisateurs, key=lambda user: user.leads.filter(statut='en_cours').count())
    # Assigner le lead à cet utilisateur
    lead.assigned_user = utilisateur_disponible
    lead.save()