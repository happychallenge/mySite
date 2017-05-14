# master/views.py
from django.shortcuts import render

# Create your views here.
def master_home(request):
    return render(request, 'base.html')