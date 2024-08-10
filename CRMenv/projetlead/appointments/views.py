from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer



def calendar(request):
    events = Event.objects.all()
    return render(request, 'appoitementfile/calendar.html', {'events': events})



def event_list(request):
    # Récupérer tous les événements depuis la base de données
    events = Event.objects.all()

    # Préparer une liste d'événements au format que FullCalendar attend
    event_data = []
    for event in events:
        event_data.append({
            'id': event.id,
            'title': event.title,   # Titre de l'événement
            'date':event.date,       
            'heure':event.heure, # Date et heure 
            'lieu':event.lieu,   # Lieu de l'événement
           
        })

    # Retourner les données des événements en JSON
    return JsonResponse(event_data, safe=False)



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


