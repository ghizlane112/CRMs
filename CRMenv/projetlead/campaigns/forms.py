from django import forms
from .models import Campaign

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'contact_email', 'start_date', 'end_date', 'budget', 'nom_entreprise']
