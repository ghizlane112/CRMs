from django import forms
from .models import Message
from .models import Note



class MessageForm(forms.ModelForm):
     class Meta:
         model = Message
         fields = ['receiver', 'lead', 'content']


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your note here...'}),
        }



