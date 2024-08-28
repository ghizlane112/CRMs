from django import forms
from .models import Message
from lead.models import Lead

class MessageForm(forms.ModelForm):
    lead = forms.ModelChoiceField(queryset=Lead.objects.all(), required=False, empty_label="Select a lead")

    class Meta:
        model = Message
        fields = ['receiver', 'content', 'lead']
