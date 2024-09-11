from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Event, History, DeletedEvent
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date, parse_time
from django.core.exceptions import ValidationError
from django.db import IntegrityError

@login_required
def calendar_view(request):
    if request.method == 'GET':
        return render(request, 'events/calendar.html')

@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        heur = request.POST.get('heur')
        lieu = request.POST.get('lieu')
        description = request.POST.get('description')

        event = Event(
            title=title,
            start_date=start_date,
            heur=heur,
            lieu=lieu,
            description=description
        )
        event.save()

        History.objects.create(
            event=event,
            action='add',
            reason='Ajout de l\'événement',
            user=request.user,
            timestamp=timezone.now()
        )

        return JsonResponse({'status': 'success'})
    


@login_required
@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        title = request.POST.get('title')
        start_date_str = request.POST.get('start_date')
        heur_str = request.POST.get('heur')
        lieu = request.POST.get('lieu')
        description = request.POST.get('description')

        try:
            # Convertir les chaînes de caractères en objets date et time
            start_date = parse_date(start_date_str)
            heur = parse_time(heur_str)
            
            if not start_date or not heur:
                return JsonResponse({'status': 'error', 'message': 'Date ou heure invalide'})

            event = get_object_or_404(Event, id=event_id)
            event.title = title
            event.start_date = start_date
            event.heur = heur
            event.lieu = lieu
            event.description = description
            event.save()

            History.objects.create(
                event=event,
                action='update',
                reason='Mise à jour de l\'événement',
                user=request.user,
                timestamp=timezone.now()
            )

            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Événement introuvable'})
        except (ValueError, ValidationError, IntegrityError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})







@login_required
@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        reason = request.POST.get('reason')
        
        try:
            event = Event.objects.get(id=event_id)
            
            DeletedEvent.objects.create(
                title=event.title,
                start_date=event.start_date,
                heur=event.heur,
                description=event.description,
                deletion_reason=reason
            )
            
            History.objects.create(
                event=event,
                action='delete',
                reason=reason,
                user=request.user,
                timestamp=timezone.now()
            )
            
            event.deleted_at = timezone.now()  # Marquer comme supprimé
            event.save()
            
            return JsonResponse({'status': 'success'})
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Événement introuvable'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})





@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def event_list(request):
    events = Event.objects.filter(deleted_at__isnull=True)
    
    events_data = [{
        'id': event.id,
        'title': event.title,
        'start': f"{event.start_date}T{event.heur}",
        'extendedProps': {
            'lieu': event.lieu,
            'description': event.description
        }
    } for event in events]
    
    return JsonResponse(events_data, safe=False)


@login_required
def history_view(request):
    today = timezone.now().date()

    # Récupérer les événements passés et futurs (non supprimés)
    past_events = Event.objects.filter(start_date__lt=today, deleted_at__isnull=True)
    future_events = Event.objects.filter(start_date__gte=today, deleted_at__isnull=True)

    # Récupérer l'historique complet (ajout, modification, suppression)
    histories = History.objects.filter(action__in=['add', 'update', 'delete']).order_by('-timestamp')

    past_event_data = []
    for event in past_events:
        action_history = History.objects.filter(event=event).last()
        past_event_data.append({
            'id': event.id,
            'title': event.title,
            'start_date': event.start_date,
            'start_time': event.heur,
            'location': event.lieu,
            'description': event.description,
            'action': action_history.action if action_history else 'Aucune action',
            'user': action_history.user.username if action_history and action_history.user else 'Inconnu'
        })

    future_event_data = []
    for event in future_events:
        action_history = History.objects.filter(event=event).last()
        future_event_data.append({
            'id': event.id,
            'title': event.title,
            'start_date': event.start_date,
            'start_time': event.heur,
            'location': event.lieu,
            'description': event.description,
            'action': action_history.action if action_history else 'Aucune action',
            'user': action_history.user.username if action_history and action_history.user else 'Inconnu'
        })

    context = {
        'past_event_data': past_event_data,
        'future_event_data': future_event_data,
        'histories': histories,  # Historique des actions (ajout, modification, suppression)
    }

    return render(request, 'events/history.html', context)




@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Récupérer tout l'historique lié à cet événement
    histories = History.objects.filter(event=event).order_by('-timestamp')

    context = {
        'event': event,
        'histories': histories,
    }

    return render(request, 'events/event_detail.html', context)





