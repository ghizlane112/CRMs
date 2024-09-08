# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from lead.models import Lead
from notification.models import Notification  # Importer le modèle Notification
from django.contrib.auth import get_user_model
from django.db.models import Q

from django.core.exceptions import PermissionDenied

@login_required
def inbox(request):
    user_id = request.GET.get('user')
    
    # Vérifier si user_id est un nombre entier et non None
    if user_id and user_id.isdigit():
        user_id = int(user_id)
        messages = Message.objects.filter(
            Q(sender_id=user_id, receiver=request.user) |
            Q(sender=request.user, receiver_id=user_id)
        ).order_by('timestamp')
    else:
        # Si aucun user_id valide, utilisez une valeur par défaut ou faites une autre action
        messages = Message.objects.filter(receiver=request.user).order_by('timestamp')

    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)
    leads = Lead.objects.all()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()

            Notification.objects.create(
                recipient=message.receiver,
                sender=request.user,
                message=f"Vous avez reçu un nouveau message de {request.user.username}: {message.content}"
            )

            return redirect(f'{request.path}?user={message.receiver.id}')
    else:
        form = MessageForm()

    return render(request, 'communication/messages.html', {
        'messages': messages,
        'users': users,
        'form': form,
        'leads': leads
    })
