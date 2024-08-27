from django.shortcuts import render

# Create your views here.
from .models import CompanyPublicitaire

def campaign_list(request):
    campaigns = CompanyPublicitaire.objects.all()
    context = {
        'campaigns': campaigns,
    }
    return render(request, 'campaigns/campaign_list.html', context)
