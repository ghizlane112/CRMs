from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from lead.models import Lead
from notification.models import Notification
from django.contrib.auth import get_user_model
from django.db.models import Q

@login_required
def inbox(request):
    user_id = request.GET.get('user')
    if user_id:
        messages = Message.objects.filter(
            (Q(sender_id=user_id) & Q(receiver=request.user)) |
            (Q(sender=request.user) & Q(receiver_id=user_id))
        ).order_by('timestamp')
    else:
        messages = Message.objects.filter(receiver=request.user).order_by('timestamp')
    
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)
    
    # Passer les leads au contexte
    leads = Lead.objects.all()
    return render(request, 'communication/messages.html', {'messages': messages, 'users': users, 'leads': leads})

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
    leads = Lead.objects.all()  # Assurez-vous de passer les leads ici aussi
    return render(request, 'communication/messages.html', {'form': form, 'leads': leads})
