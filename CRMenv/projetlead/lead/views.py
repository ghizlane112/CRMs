from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from .models import Lead
from django.views.generic import ListView
from .forms import LeadSortForm
from .forms import LeadForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import LeadSerializer
from .models import Interaction, Lead
from .forms import InteractionForm
from django.db.models import Q

# Create your views here.
def one(request):
    return render(request,'principale.html')

def two(request):
    return render(request,'parts/nav.html')

def three(request):
    return render(request,'parts/button.html')

def four(request):
    return render(request,'dashboard.html')



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
    paginator = Paginator(leads, 5)  # 5 leads par page
    page_number = request.GET.get('page', 1)  # Utiliser 1 comme page par défaut

    try:
        leads_page = paginator.get_page(page_number)
    except PageNotAnInteger:
        leads_page = paginator.get_page(1)  # Page 1 si la page demandée n'est pas un entier
    except EmptyPage:
        leads_page = paginator.get_page(paginator.num_pages)  # Dernière page si la page demandée est vide



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





def interaction_list(request):
    interactions = Interaction.objects.all()
    return render(request, 'leadfile/interaction_list.html', {'interactions': interactions})

class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer






