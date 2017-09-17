from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ReportForm

# Create your views here.
def add_report(request):

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "오류가 보고 되었습니다.")
            return redirect('home')

    else:
        if request.user:
            email = request.user.username
        form = ReportForm(initial={'email':email})

    return render(request, 'mistake/add_report.html', {'form':form})
