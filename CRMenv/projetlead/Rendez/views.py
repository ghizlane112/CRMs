from django.shortcuts import render
from django.http import JsonResponse
from .models import Event
import logging
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
        description = request.POST.get('description')

        event = Event(
            title=title,
            start_date=start_date,
            heur=heur,
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
        description = request.POST.get('description')

        event = get_object_or_404(Event, id=event_id)
        event.title = title
        event.start_date = start_date
        event.heur = heur
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
