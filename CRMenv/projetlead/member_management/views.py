# member_management/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import MemberCreationForm

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def add_member(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarde le membre avec l'email et le mot de passe saisis
            return redirect('dashboard')  # Redirige vers le tableau de bord ou une autre page
    else:
        form = MemberCreationForm()

    return render(request, 'member_management/add_member.html', {'form': form})