from django import forms
from .models import Report
from datetime import date

class ReportForm(forms.ModelForm):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    category = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Report
        fields = ['title', 'content', 'report_type']

    def save(self, commit=True):
        report = super().save(commit=False)
        filters = {
            'start_date': self.cleaned_data.get('start_date').strftime('%Y-%m-%d') if self.cleaned_data.get('start_date') else None,
            'end_date': self.cleaned_data.get('end_date').strftime('%Y-%m-%d') if self.cleaned_data.get('end_date') else None,
            'category': self.cleaned_data.get('category')
        }
        # Supprimer les valeurs None pour éviter d'enregistrer des clés avec des valeurs nulles
        filters = {k: v for k, v in filters.items() if v is not None}
        report.filters = filters
        if commit:
            report.save()
        return report
