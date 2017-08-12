# records/views_reg.py
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from mySite.decorators import ajax_required
from mySite.master.models import Media, Job
from .models import News, Tag
from .get_news import get_news
from .get_person import get_person_info
from .models import Evidence, Person, Event, PersonEvent, Evidence
from .forms import PersonForm, EventForm, EvidenceForm, PersonEvidenceForm


@login_required
def check_person(request):
    if request.method == 'POST':
        name = request.POST.get('person')
        person_list = Person.objects.prefetch_related('personevent_set').filter(name=name)
        return render(request, 'records/check_person_result.html', {
                'person_list': person_list, 'name':name
            })
    else:
        return render(request, 'records/check_person.html')


@login_required
def add_person(request):
    if request.method == 'POST':
        tag_array = []
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            person = form.save()
            name = form.cleaned_data.get('name')
            event = form.cleaned_data.get('event')
            url = form.cleaned_data.get('url')

            # Jobs
            jobs = form.cleaned_data.get('jobs')
            if jobs:
                person.jobs.set(jobs)
            person.created_user = request.user

            # Tags
            tags = form.cleaned_data.get('tags')
            if tags:
                tag_list = tags.split(',')
                for tag in tag_list:
                    tag = tag.strip()
                    tagged, created = Tag.objects.get_or_create(tag=tag)
                    tag_array.append(tagged)
                person.tags.set(tag_array)

            person.save()
            return redirect('records:check_event', person.id)
    else:
        person = request.GET.get('person')
        form = PersonForm(initial={'name':person})
    return render(request, 'records/add_person.html', {'form':form})


@login_required
def check_event(request, person_id):
    if request.method == 'POST':
        name = request.POST.get('event')
        person = get_object_or_404(Person, id=person_id)
        event_list = Event.objects.prefetch_related('personevent_set').filter(tags=name)
        return render(request, 'records/check_event_result.html', {
                'event_list': event_list, 'person':person
            })
    else:
        person = get_object_or_404(Person, id=person_id)
        return render(request, 'records/check_event.html', {'person':person})


@login_required
def person_event_matching(request, person_id):
    if request.method == 'POST':
        event_id = request.POST.get('event')
        person = get_object_or_404(Person, id=person_id)
        event = get_object_or_404(Event, id=event_id)

        PersonEvent.objects.create(person=person, event=event, created_user=request.user)
       
        return redirect('records:person_detail', person.id)
    else:
        person = get_object_or_404(Person, id=person_id)
        return render(request, 'records/check_event.html', {'person':person})



@login_required
def add_event(request, person_id):
    tag_array = []
    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save()

            tags = form.cleaned_data.get('tags')
            if tags:
                tag_list = tags.split(',')
                for tag in tag_list:
                    tag = tag.strip()
                    tagged, created = Tag.objects.get_or_create(tag=tag)
                    tag_array.append(tagged)
                event.tags.set(tag_array)

            person = get_object_or_404(Person, id=person_id)

            personevent = PersonEvent.objects.create(
                    person=person, event=event, created_user=request.user)

        return redirect('records:check_evidence', personevent.id)
    else:
        form = EventForm(initial={'person':person_id})
    return render(request, 'records/add_event.html', {
            'form':form, 'person':person_id
        })

###################################
# 

@login_required
def check_evidence(request, personevent_id):

    if request.method == 'POST':
        form = EvidenceForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data.get('url')

            # 뉴스의 결과물를 보여 주기 위해 DB에 입력한다.
            if News.objects.filter(url=url).count():
                news = get_object_or_404(News, url=url)
            
            else:
                news_info = get_news(url)
                media = get_object_or_404(Media, short=news_info['media'])
                content = news_info['content'][:400] + ' ......'
                news = News.objects.create(
                            url=url, 
                            media=media, 
                            title=news_info['title'], 
                            content=content, 
                            published_at=news_info.get('published_at', "1900-01-01"),
                            created_user=request.user,
                        )
            
            personevent = PersonEvent.objects.select_related('person', 'event').get(id=personevent_id)
            # Form 을 만들어 보내서 OK가 누르면 바로 입력이 되도록 한다.
            form = PersonEvidenceForm(initial={'personevent': personevent_id, 'news':news.id})
            return render(request, 'records/check_evidence_result.html',{
                    'form':form, 'personevent':personevent_id, 'news': news, 
                    'person':personevent.person, 'event':personevent.event
                })

    personevent = PersonEvent.objects.select_related('person', 'event').get(id=personevent_id)

    return render(request, 'records/check_evidence.html', {
            'personevent':personevent_id, 'person':personevent.person, 'event':personevent.event
        })


@login_required
def add_evidence(request):
    if request.method == "POST":

        personevent_id = request.POST.get('personevent')
        news_id = request.POST.get('news')

        personevent = PersonEvent.objects.select_related('person').get(id=personevent_id)
        news = get_object_or_404(News, id=news_id)

        Evidence.objects.create(personevent=personevent, news=news, created_user=request.user)

        return redirect('records:person_detail', personevent.person.id)



@login_required
def add_news(request):
    form = PersonEventNewsForm()
    return render(request, 'records/add_news.html', {'form': form})


@login_required
def add_news_result(request, person=None, event=None, url=None):
    evidence_list = None
    person_list = None
    event_list = None
    news = None

    if request.method == 'POST':
        form = PersonEventNewsForm(request.POST)

        if form.is_valid():
            person = form.cleaned_data.get('person')
            event = form.cleaned_data.get('event')
            url = form.cleaned_data.get('url')

    if News.objects.filter(url=url).count():
        news_info = get_news(url)
        content = news_info['content']
        if not content.count(person):
            form = PersonEventNewsForm(initial={'event': event, 'url':url})
            error_message="해당 뉴스에는 '{}'란 이름이 없습니다. 다시 입력해 주시기 바랍니다.".format(person)
            return render(request, 'records/add_news.html', {
                        'form': form, 'error_messages': error_message
                })

        news = get_object_or_404(News, url=url)
        if news.content.count(person):
            try:
                person_list = Person.objects.prefetch_related('personevent_set').filter(name=person)
            except Person.DoesNotExist:
                raise Http404
    else:
        news_info = get_news(url)
        content = news_info['content']
        if content.count(person):
            media = get_object_or_404(Media, short=news_info['media'])
            content = content[:400] + ' ......'
            news = News.objects.create(
                        url=url, 
                        media=media, 
                        title=news_info['title'], 
                        content=content, 
                        published_at=news_info.get('published_at', ""),
                        created_user=request.user,
                    )
        else:
            form = PersonEventNewsForm(initial={'event': event, 'url':url})
            error_message="해당 뉴스에는 '{}'란 이름이 없습니다. 다시 입력해 주시기 바랍니다.".format(person)
            return render(request, 'records/add_news.html', {
                        'form': form, 'error_messages': error_message
                })

    events = event.split(' ')
    try:
        event_list = Event.objects.filter(name__contains=events)
    except Person.DoesNotExist:
        raise Http404

    try:
        evidence_list = Evidence.objects.select_related('personevent').filter(news=news)
    except Person.DoesNotExist:
        raise Http404

    return render(request, 'records/add_news_result.html', {
            'person': person,
            'event': event,
            'url': url,
            'news': news,
            'evidence_list': evidence_list,
            'person_list': person_list,
            'event_list': event_list,
        })





# @login_required
# def person_news(request):
#     if request.method == 'POST':
#         form = PersonNewsForm(request.POST)
#         if form.is_valid():

