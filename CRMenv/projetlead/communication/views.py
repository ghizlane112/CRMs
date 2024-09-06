# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

from .forms import MessageForm
from lead.models import Lead

from notification.models import Notification  # Importer le modèle Notification
from django.contrib.auth import get_user_model
from django.db.models import Q




@login_required
def inbox(request):
    user_id = request.GET.get('user')
    
    # Récupérer les messages entre l'utilisateur courant et le contact sélectionné
    if user_id:
        messages = Message.objects.filter(
            Q(sender_id=user_id, receiver=request.user) |
            Q(sender=request.user, receiver_id=user_id)
        ).order_by('timestamp')
    else:
        messages = Message.objects.filter(receiver=request.user).order_by('timestamp')

    # Liste des autres utilisateurs (pour afficher dans la liste des contacts)
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)
    
    # Leads (optionnel si nécessaire pour le formulaire)
    leads = Lead.objects.all()

    # Si la requête est POST, gérer l'envoi du message
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            # Créez une notification après l'envoi du message
            Notification.objects.create(
                recipient=message.receiver,
                sender=request.user,
                message=f"Vous avez reçu un nouveau message de {request.user.username}: {message.content}"
            )

            # Redirige vers la même conversation après l'envoi du message
            return redirect(f'{request.path}?user={message.receiver.id}')
    else:
        form = MessageForm()

    return render(request, 'communication/messages.html', {
        'messages': messages,
        'users': users,
        'form': form,
        'leads': leads
    })

