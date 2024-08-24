from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReportForm
from .models import Report
#import pandas as pd
#import io
#import openpyxl
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas


from django.http import HttpResponse




def report_view(request, report_id=None):
    if report_id:
        # Affichage des détails d'un rapport spécifique
        report = get_object_or_404(Report, id=report_id)
        return render(request, 'reports/report_detail.html', {'report': report})

    report_type = request.GET.get('report_type')

    if report_type in ['conversion', 'campaign_performance', 'interaction']:
        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                report = form.save(commit=False)
                report.created_by = request.user
                report.report_type = report_type
                # `filters` est déjà géré dans le formulaire
                report.save()
                return redirect('report_dashboard')
        else:
            form = ReportForm()

        return render(request, 'reports/report_form.html', {
            'form': form,
            'report_type': {
                'conversion': 'Rapport de Conversion',
                'campaign_performance': 'Rapport de Performance des Campagnes',
                'interaction': 'Rapport de Suivi des Interactions'
            }.get(report_type, 'Rapport')
        })

    if request.GET.get('action') == 'history':
        reports = Report.objects.filter(created_by=request.user)
        return render(request, 'reports/report_history.html', {'reports': reports})

    report_options = [
        {'name': 'Rapport de Conversion', 'url': '?report_type=conversion'},
        {'name': 'Rapport de Performance des Campagnes', 'url': '?report_type=campaign_performance'},
        {'name': 'Rapport de Suivi des Interactions', 'url': '?report_type=interaction'},
        {'name': 'Voir Historique des Rapports', 'url': '?action=history'},
    ]
    return render(request, 'reports/report_dashboard.html', {'report_options': report_options})











