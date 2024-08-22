from django.shortcuts import render
from django.http import JsonResponse
from .models import Event
import logging
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

#logger = logging.getLogger(__name__)

def calendar_view(request):
    if request.method == 'GET':
        # Renvoie la page HTML du calendrier
        return render(request, 'events/calendar.html')
   

@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        heur = request.POST.get('heur')
        lieu=request.POST.get('lieu')
        description = request.POST.get('description')

        event = Event(
            title=title,
            start_date=start_date,
            heur=heur,
            lieu=lieu,
            description=description
        )
        event.save()
        return JsonResponse({'status': 'success'})


@csrf_exempt
def update_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        heur = request.POST.get('heur')
        lieu=request.POST.get('lieu')
        description = request.POST.get('description')

        event = get_object_or_404(Event, id=event_id)
        event.title = title
        event.start_date = start_date
        event.heur = heur
        event.lieu=lieu
        event.description = description
        event.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Méthode de requête invalide'})


@csrf_exempt
def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('id')
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Méthode de requête invalide'})







def dashboard_view(request):
    return render(request, 'dashboard.html')



def event_list(request):
    # Renvoie les événements en JSON pour FullCalendar
    events = Event.objects.all()
    events_data = [{
        'id': event.id,
        'title': event.title,
        'start': f"{event.start_date}T{event.heur}",  # Combine la date et l'heure pour FullCalendar
        'description': event.description,
    } for event in events]
    return JsonResponse(events_data, safe=False)





def history_view(request):
    today = timezone.now().date()
    past_events = Event.objects.filter(start_date__lt=today)
    future_events = Event.objects.filter(start_date__gte=today)
    
    context = {
        'past_events': past_events,
        'future_events': future_events,
    }
    
    return render(request, 'events/history.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)

