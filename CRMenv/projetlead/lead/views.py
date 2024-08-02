from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Lead
from .forms import LeadForm

# Create your views here.
def one(request):
    return render(request,'principale.html')

def two(request):
    return render(request,'parts/nav.html')

def three(request):
    return render(request,'parts/button.html')




def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'leadfile/lead_list.html', {'leads': leads})

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

    return render(request, 'leads/lead_import.html')