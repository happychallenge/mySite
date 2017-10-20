# records/views_reg.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from mySite.decorators import ajax_required
from mySite.master.models import Media, Job
from .models import News, Event
from .get_news import get_news
# from .models import Evidence, Person, Event, PersonEvent, Evidence
# from .forms import PersonForm, EventForm, EvidenceForm, PersonEvidenceForm


@login_required
def add_event_news(request, event_id):

    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        url = request.POST.get('url')

        # 뉴스의 결과물를 보여 주기 위해 DB에 입력한다.
        if News.objects.filter(url=url).count():
            news = get_object_or_404(News, url=url)
        
        else:
            news_info = get_news(url)
            try:
                media = get_object_or_404(Media, short=news_info['media'])
            except Media.DoesNotExists:
                media = get_object_or_404(Media, short='기타')
            
            content = news_info['content'][:400] + ' ......'
            news, created = News.objects.get_or_create(
                    url=url, 
                    media=media, 
                    title=news_info['title'], 
                    content=content, 
                    published_at=news_info.get('published_at', "1900-01-01"),
                    created_user=request.user,
                )

        event.eventnews.add(news)
        return redirect('records:event_detail', event_id)


    else:
        return render(request, 'records/add_event_news.html', {'event':event})
