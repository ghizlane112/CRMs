# member_management/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Member1User  # Importez le modèle User depuis l'application users

class MemberCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Member1User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']