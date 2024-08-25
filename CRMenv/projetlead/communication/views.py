# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from notification.models import Notification  # Importer le modèle Notification

@login_required
def inbox(request):
    # Récupère les messages reçus par l'utilisateur connecté
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'communication/messages.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            # Créez une notification
            Notification.objects.create(
                recipient=message.receiver,
                sender=request.user,
                message=f"Vous avez reçu un nouveau message de {request.user.username}: {message.content}"
            )
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'communication/messages.html', {'form': form})