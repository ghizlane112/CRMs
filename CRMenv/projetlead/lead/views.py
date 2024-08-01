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