from django import forms
from .models import Lead
import csv
from io import StringIO

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nom', 'prenom', 'email', 'telephone', 'source', 'statut', 'note']


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

