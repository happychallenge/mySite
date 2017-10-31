# records/views_reg.py
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib import messages

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
            if not person.nick_name:
                person.nick_name = name
                    
            person.created_user = request.user
            person.save()

            # Jobs
            jobs = form.cleaned_data.get('jobs')
            if jobs:
                person.jobs.set(jobs)

            # Tags
            tags = form.cleaned_data.get('tags')
            if tags:
                tag_list = tags.split(',')
                for tag in tag_list:
                    tag = tag.strip()
                    tagged, created = Tag.objects.get_or_create(tag=tag)
                    tag_array.append(tagged)
                    
            tagged, created = Tag.objects.get_or_create(tag=name)
            tag_array.append(tagged)
            person.tags.set(tag_array)
            
            messages.success(request, "{} 이 추가 되었습니다.".format(name))
            return redirect('records:check_event', person.id)
    else:
        person = request.GET.get('person')
        form = PersonForm(initial={'name':person})
    return render(request, 'records/add_person.html', {'form':form})


@login_required
def edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        tag_array = []
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person = form.save()
            name = form.cleaned_data.get('name')

            # person.save_m2m()
            # # Jobs
            # jobs = form.cleaned_data.get('jobs')
            # if jobs:
            #     person.jobs.set(jobs)

            # # Jobs
            # tags = form.cleaned_data.get('tags')
            # if tags:
            #     person.tags.set(tags)

            person.created_user = request.user
            person.save()
            
            messages.success(request, "{} 이 수정 되었습니다.".format(name))
            return redirect('records:person_detail', person.id)
    else:
        form = PersonForm(instance=person)
    return render(request, 'records/add_person.html', {'form':form})


@login_required
def check_event(request, person_id):
    if request.method == 'POST':
        tag = request.POST.get('event')
        person = get_object_or_404(Person, id=person_id)
        event_list = Event.objects.filter(tags__tag__contains=tag)
        return render(request, 'records/check_event_result.html', {
                'event_list': event_list, 'person':person, 'tag':tag
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

        PersonEvent.objects.get_or_create(person=person, event=event, created_user=request.user)
       
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

            messages.success(request, "{} 이 추가 되었습니다.".format(event.name))

            person = get_object_or_404(Person, id=person_id)

            personevent = PersonEvent.objects.get_or_create(
                    person=person, event=event, created_user=request.user)

        return redirect('records:check_evidence', personevent.id)
    else:
        form = EventForm(initial={'person':person_id})
    return render(request, 'records/add_event.html', {
            'form':form, 'person':person_id
        })


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
            
            personevent = PersonEvent.objects.get(id=personevent_id)
            # Form 을 만들어 보내서 OK가 누르면 바로 입력이 되도록 한다.
            form = PersonEvidenceForm(initial={'personevent': personevent.id, 'news':news.id })
            return render(request, 'records/check_evidence_result.html',{
                    'form':form, 'personevent':personevent, 'news': news, 
                })

    personevent = PersonEvent.objects.select_related('person', 'event').get(id=personevent_id)

    return render(request, 'records/check_evidence.html', {
            'personevent':personevent,
        })


@login_required
def add_evidence(request):
    if request.method == "POST":

        personevent_id = request.POST.get('personevent')
        news_id = request.POST.get('news')

        personevent = get_object_or_404(PersonEvent, id=personevent_id)
        news = get_object_or_404(News, id=news_id)

        Evidence.objects.get_or_create(personevent=personevent, news=news, created_user=request.user)

        messages.success(request, "{} 이 {} 사건에 뉴스를 추가 하었습니다.".format(
                    personevent.person.name, personevent.event.name))

        return redirect('records:person_detail', personevent.person.id)


############################
# Register Relationship
############################
def evidence_add_person(request, news_id, event_id):
    news = get_object_or_404(News, id=news_id)
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        persons_id = request.POST.getlist('persons_id')

        if persons_id:
            for person_id in persons_id:
                person = get_object_or_404(Person, id=person_id)
                obj, created = PersonEvent.objects.get_or_create(person=person, event=event, created_user=request.user)
                Evidence.objects.get_or_create(personevent=obj, news=news, created_user=request.user)

                messages.success(request, "{} 이 {} 뉴스에 추가 되었습니다.".format(
                    person.name, news.title))

    return redirect('records:person_detail', person_id)
        