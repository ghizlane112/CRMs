from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from .models import Lead, Interaction
import csv
from .forms import InteractionForm
from django.views.generic import ListView
from .forms import LeadSortForm
from .forms import LeadForm, NoteForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import LeadSerializer
from django.db.models import Q

# Create your views here.
def one(request):
    return render(request,'principale.html')



def two(request):
    return render(request,'parts/nav.html')

def three(request):
    return render(request,'parts/button.html')

def dashboard(request):
    return render(request,'dashboard.html')



def four(request):
    return render(request,'parts/state.html')


def lead_list(request):
    leads = Lead.objects.all()

    #return render(request, 'leadfile/lead_list.html', {'leads': leads})
    search_text = request.GET.get('search', '')
    sort_field = request.GET.get('sort', '')


    # Appliquer les filtres si le texte de recherche est présent
    if search_text:
        leads = leads.filter(
            Q(nom__icontains=search_text) |
            Q(prenom__icontains=search_text) |
            Q(email__icontains=search_text) |
            Q(telephone__icontains=search_text) |
            Q(source__icontains=search_text) |
            Q(statut__icontains=search_text) |
            Q(note__icontains=search_text)
        )


     # Appliquer le tri si un champ de tri est sélectionné
    if sort_field:
        leads = leads.order_by(sort_field)
    # Rendre les options de filtre disponibles pour le template

    # Pagination
    paginator = Paginator(leads, 8)  # 5 leads par page
    page_number = request.GET.get('page')  # Utiliser 1 comme page par défaut

    try:
        leads = paginator.get_page(page_number)
    except PageNotAnInteger:
        leads = paginator.get_page(1)  # Page 1 si la page demandée n'est pas un entier
    except EmptyPage:
        leads = paginator.get_page(paginator.num_pages)  # Dernière page si la page demandée est vide



    return render(request, 'leadfile/lead_list.html', {
        'leads': leads,
        'search_text': search_text,
        'sort_field': sort_field
    })









#### pour details
def lead_detail(request, pk):
    lead = Lead.objects.get(pk=pk)
    return render(request, 'leadfile/lead_detail.html', {'lead': lead})

def lead_create(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'leadfile/lead_form.html', {'form': form})




def lead_import(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            # Handle error
            return redirect('lead_list')
        
        # Read and process CSV file
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        
        for row in reader:
            Lead.objects.create(
                nom=row['Nom'],
                prenom=row['Prénom'],
                email=row['Email'],
                telephone=row['Téléphone'],
                source=row['Source'],
                statut=row['Statut'],
                note=row.get('Note', '')
            )
        return redirect('lead_list')

    return render(request, 'leadfile/import_leads.html')




def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    return redirect('lead_list')




def lead_edit(request, id):
    lead = get_object_or_404(Lead, id=id)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'leadfile/lead_edit.html', {'form': form})


class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer




def interaction_list(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    interactions = lead.interactions.all()
    return render(request, 'lead/interaction_list.html', {'lead': lead, 'interactions': interactions})

def add_interaction(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        form = InteractionForm(request.POST)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.lead = lead
            interaction.utilisateur = request.user
            interaction.save()
            return redirect('interaction_list', lead_id=lead.id)
    else:
        form = InteractionForm()
    return render(request, 'lead/add_interaction.html', {'form': form, 'lead': lead})




def add_note(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.lead = lead
            note.user = request.user  # Associe la note à l'utilisateur actuel
            note.save()
            return redirect('lead_detail', pk=pk)  # Redirige vers les détails du lead
    else:
        form = NoteForm()  # Formulaire vide pour GET ou après une soumission réussie
    
    # Récupère les notes associées au lead pour l'affichage
    notes = lead.notes.all()
    
    return render(request, 'leadfile/ajouter-note.html', {
        'lead': lead,
        'notes': notes,
        'form': form
    })
