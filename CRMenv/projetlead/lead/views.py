from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
def one(request):
    return render(request,'principale.html')