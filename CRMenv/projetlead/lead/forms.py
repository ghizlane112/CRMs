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
        


