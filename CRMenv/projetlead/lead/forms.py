from django import forms
from .models import Lead
import csv
from io import StringIO
from django.contrib.auth.models import User
from .models import Interaction

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nom', 'prenom', 'email', 'telephone', 'source', 'statut', 'note','responsable']

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.all()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Lead.objects.filter(email=email).exists():
            raise forms.ValidationError("Un lead avec cet email existe déjà.")
        return email



class LeadSortForm(forms.Form):
    SORT_CHOICES = [
        ('first_name', 'Prénom'),
        ('last_name', 'Nom'),
        ('email', 'Email'),
        ('phone', 'Téléphone'),
        ('source', 'Source'),
        ('status', 'Statut'),
        ('created_at', 'Date de création'),
    ]
    ordering = forms.ChoiceField(choices=SORT_CHOICES, required=True, label='Trier par')



class CSVImportForm(forms.Form):
   csv_file = forms.FileField()
   
   def handle_uploaded_file(self, file):
        file_content = file.read().decode('utf-8')
        csv_file = StringIO(file_content)
        reader = csv.DictReader(csv_file)
        for row in reader:
            Lead.objects.create(
               nom=row['nom'],
                prenom=row['prenom'],
                email=row['email'],
                telephone=row['telephone'],
                source=row['source'],
                statut=row['statut'],
                note=row.get('note', ''),
            )



class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['type', 'date', 'description', 'lead', 'user']



