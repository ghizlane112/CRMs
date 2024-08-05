from django.contrib import admin
from .models import Lead
# Register your models here.

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'source', 'statut', 'note', 'date_creation')
    search_fields = ('nom', 'prenom', 'email', 'telephone')


