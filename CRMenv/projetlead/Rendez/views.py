from django.shortcuts import render
from django.http import JsonResponse
from .models import Event

def calendar_view(request):
    if request.method == 'GET':
        # Renvoie la page HTML du calendrier
        return render(request, 'events/calendar.html')
    elif request.method == 'POST':
        # Ajoute un événement à la base de données
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
