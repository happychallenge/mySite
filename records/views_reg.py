# records/views_reg.py
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from decorators import ajax_required
from .models import News
from .get_news import get_news

@login_required
def evidence_create(request):
    return render(request, 'records/evidence_create.html')

@login_required
@ajax_required
def evidence_records(request):
    html = ''
    url = request.POST.get('url')
    if url:
        result = get_news(url)
        news = News.objects.filter(url=url)
        if news:
            personevent = Evidence.objects.select_related('personevent').filter(news=news)

    html = '{0}{1}'.format(html, render_to_string('records/news.html', {
            'result': result,
            'personevent': personevent,
        }))

    return HttpResponse(html)
