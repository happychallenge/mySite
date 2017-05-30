# records/views_reg.py
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from decorators import ajax_required
from master.models import Media
from .models import News
from .get_news import get_news
from .get_person import get_person_info
from .models import Evidence, Person, Event

@login_required
def evidence_create(request):
    return render(request, 'records/evidence_create.html')

@login_required
@ajax_required
def check_person_ajax(request):

    html = ''
    names = request.POST.get('persons')
    names = names.strip().split(',')
    for name in names:
        name = name.strip()
        person_list = Person.objects.filter(name=name)

        html = '{0}{1}'.format(html, render_to_string('records/partial_persons.html', {
                'person_list':person_list,
        }))

    return HttpResponse(html)


@login_required
@ajax_required
def check_event_ajax(request):

    html = ''
    events = request.POST.get('events')
    events = events.strip().split(',')
    for event in events:
        event = event.strip()
        event_list = Event.objects.filter(name__contains=event)

        html = '{0}{1}'.format(html, render_to_string('records/partial_events.html', {
                'event_list':event_list,
        }))

    return HttpResponse(html)

@login_required
@ajax_required
def evidence_records(request):

    html = ''
    news = None
    evidence_list = None

    url = request.POST.get('url')
    
    if url:
        count = News.objects.filter(url=url).count()
        if count:
            news = get_object_or_404(News, url=url)
            evidence_list = Evidence.objects.select_related('personevent').filter(news=news)
        else:
            news = get_news(url)
            media = Media.objects.get(short=news['media'])
            news, created = News.objects.get_or_create(
                            url=url, 
                            media=media, 
                            title=news['title'], 
                            content=news['content'], 
                            published_at=news['published_at'],
                            created_user=request.user,
                        )

        html = '{0}{1}'.format(html, render_to_string('records/partial_news.html', {
                'news': news,
                'evidence_list': evidence_list,
            }))
        return HttpResponse(html)
    else:
        return HttpResponse('URL을 다시 입력하세요.')
