# records/views.py
from datetime import timedelta, datetime
# from django.utils import timezone

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Person, PersonEvent, Event, Tag, Relationship

# Create your views here.
def check_session(request):

    now = datetime.now()
    if 'popular_tags' in request.session:
        dt, _ = request.session.get('reg_time').split('.')
        reg_time = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        if now < reg_time:
            return False
  
    request.session.set_expiry(int(timedelta(days=365).total_seconds()))
    request.session['popular_tags'] = Tag.get_person_popular_tags()
    request.session['pop_persons'] = Person.get_persons_following()
    request.session['new_persons'] = Person.get_new_persons()
    request.session['reg_time'] = str(now)
    print(str(now))
    return True


def _person_list(request, person_list, template='records/person_list.html'):
    
    paginator = Paginator(person_list, 6)
    page = request.GET.get('page')

    try:
        person_list = paginator.page(page)
    except PageNotAnInteger:
        person_list = paginator.page(1)
    except EmptyPage:
        person_list = paginator.page(paginator.num_pages)

    check_session(request)
    context = {'person_list': person_list}
    return render(request, template, context)


def person_list(request):
    person_list = Person.objects.annotate(
            num_following=Count('following')).filter(status='P').order_by('-num_following')
    return _person_list(request, person_list)

def ajax_person_list(request):
    person_list = Person.objects.annotate(
            num_following=Count('following')).filter(status='P').order_by('-num_following')
    return _person_list(request, person_list, 
            template='records/partial/partial_person_list.html')

def person_table(request):
    person_list = Person.objects.prefetch_related('tags', 'jobs').filter(status='P')
    
    context = {'person_list': person_list}
    return render(request, 'records/person_table.html', context)

def person_detail(request, person_id):
    person = Person.objects.select_related('created_user').prefetch_related(
            'tags', 'jobs', 'personevent_set__event', 'personevent_set__evidence_set__news', 
            'user_like', 'following').get(id=person_id)
    # personevent_list = PersonEvent.objects.select_related('event', 'person').filter(person=person).all()
    check_session(request)
    context = { 'person': person }
    return render(request, 'records/person_detail.html', context)


def person_relationship(request, person_id):
    person = Person.objects.select_related('created_user').prefetch_related(
            'tags', 'jobs', 'personevent_set__event', 'personevent_set__evidence_set__news', 
            'user_like', 'following').get(id=person_id)
    # personevent_list = PersonEvent.objects.select_related('event', 'person').filter(person=person).all()
    check_session(request)
    context = { 'person': person }
    return render(request, 'records/person_relationship.html', context)


def person_family(request, person_id):
    person = Person.objects.select_related('created_user').prefetch_related(
            'tags', 'jobs', 'personevent_set__event', 'personevent_set__evidence_set__news', 
            'user_like', 'following').get(id=person_id)
    # personevent_list = PersonEvent.objects.select_related('event', 'person').filter(person=person).all()
    check_session(request)
    context = { 'person': person, }
    return render(request, 'records/person_family.html', context)

# Create your views here.
def _event_list(request, event_list):
    paginator = Paginator(event_list, 6)
    page = request.GET.get('page')

    try:
        event_list = paginator.page(page)
    except PageNotAnInteger:
        event_list = paginator.page(1)
    except EmptyPage:
        event_list = paginator.page(paginator.num_pages)
    check_session(request)
    context = { 'event_list': event_list }

    return render(request, 'records/event_list.html', context)

def event_list(request):
    event_list = Event.objects.prefetch_related('tags', 'user_like', 
            'following').select_related('category', 'created_user').annotate(
            related_person=Count('personevent')).order_by('-related_person')
    return _event_list(request, event_list)

def event_detail(request, event_id):
    event = Event.objects.select_related('category').get(id=event_id)
    personevent_list = PersonEvent.objects.select_related('person').filter(event=event).all()
    check_session(request)
    context = { 'event': event, 'personevent_list': personevent_list }
    return render(request, 'records/event_detail.html', context)


############################
# Person
############################
@login_required
@require_http_methods(["POST"])
def ajax_person_like(request, person_id):
    data = dict()
    user = request.user
    # person_id = request.POST.get('personid')
    person = get_object_or_404(Person, id=person_id)
    user_list = person.user_like.all()
    
    if user in user_list :
        person.user_like.remove(user)
        data['like'] = 'like'
        user.profile.notify_person_unliked(person)
    else:
        person.user_like.add(user)
        data['like'] = 'unlike'
        user.profile.notify_person_liked(person)

    data['status'] = True
    data['total_likes'] = person.total_likes

    return JsonResponse(data)    


@login_required
@require_http_methods(["POST"])
def ajax_person_following(request, person_id):
    data = dict()
    user = request.user

    person = get_object_or_404(Person, id=person_id)
    user_list = person.following.all()
    
    if user in user_list :
        person.following.remove(user)
        data['follow'] = 'following'
        data['message'] = '{} 님 지켜 보기을 취소하셨습니다.'.format(person.name)
        user.profile.notify_person_unfollowing(person)
    else:
        person.following.add(user)
        data['follow'] = 'unfollowing'
        data['message'] = '{} 님 지켜 보기를 신청하셨습니다.'.format(person.name)
        user.profile.notify_person_following(person)

    data['status'] = True
    data['total_following'] = person.total_following

    return JsonResponse(data)    


############################
# Event
############################
@login_required
@require_http_methods(["POST"])
def ajax_event_like(request, event_id):
    data = dict()
    # event_id = request.POST.get('eventid')
    event = get_object_or_404(Event, id=event_id)
    user_list = event.user_like.all()
    
    if request.user in user_list :
        event.user_like.remove(request.user)
        data['like'] = 'like'
    else:
        event.user_like.add(request.user)
        data['like'] = 'unlike'

    data['status'] = True
    data['total_likes'] = event.total_likes

    return JsonResponse(data)    


@login_required
@require_http_methods(["POST"])
def ajax_event_following(request, event_id):
    data = dict()
    
    event = get_object_or_404(Event, id=event_id)
    user_list = event.following.all()
    
    if request.user in user_list :
        event.following.remove(request.user)
        data['follow'] = 'following'
        data['message'] = '사건 "{}" 지켜 보기 취소하셨습니다.'.format(event.name)
    else:
        event.following.add(request.user)
        data['follow'] = 'unfollowing'
        data['message'] = '사건 "{}" 지켜 보기를 신청하셨습니다.'.format(event.name)

    data['status'] = True
    data['total_following'] = event.total_following

    return JsonResponse(data)    


############################
# Tag
############################
def tag(request, tag_name, type):
    tag = Tag.objects.get(tag=tag_name)
    if type == 'P':
        person_list = tag.person_set.all() 
        return _person_list(request, person_list)
    else:
        event_list = tag.event_set.all() 
        return _event_list(request, event_list)


############################
# Register Relationship
############################
def register_relation(request, person_id):

    me = Person.objects.get(id = person_id)
    message = ""

    if request.method == "POST":
        parent_id = request.POST.get('parent_id')
        spouse_id = request.POST.get('spouse_id')
        children_id = request.POST.getlist('children_id')

        if parent_id:
            ptype = request.POST.get('ptype')
            other = Person.objects.get(id = parent_id)
            Relationship.objects.create(person=me, other=other, relationship='parent', ctype=ptype)
            message += "{} 님이 부모님으로 추가되었습니다. <br>".format(other.name)

        if spouse_id:
            stype = request.POST.get('stype')
            other = Person.objects.get(id = spouse_id)
            Relationship.objects.create(person=me, other=other, relationship='spouse', ctype=stype)
            Relationship.objects.create(person=other, other=me, relationship='spouse', ctype=stype)
            message += "{} 님이 아내또는 남편으로 추가되었습니다. <br>".format(other.name)

        if children_id:
            for child in children_id:
                other = Person.objects.get(id = child)
                ctype = '아버지' if other.sex == 'M' else '어머니'
                Relationship.objects.create(person=other, other=me, relationship='parent', ctype=ctype)
                message += "{} 님이 아들 또는 딸로 추가되었습니다. <br>".format(other.name)

        if parent_id or spouse_id or children_id:
            messages.success(request, message)
            return redirect('records:person_relationship', person_id)
        else:
            messages.success(request, "반드시 한개 이상의 관계는 입력을 해야 합니다.")
            return redirect('records:person_relationship', person_id)


############################
# Search Person
############################
def search_persons(request):
    search_query = request.GET.get('keyword')
    if search_query:
        person_list = Person.objects.filter(name__contains = search_query)
    html = render_to_string('records/partial/search_persons.html', {
            'person_list': person_list,
        })
    return JsonResponse(html, safe=False)


############################
# TOP Search
############################
def top_search(request):
    html = ""
    search_query = request.GET.get('keyword')
    if search_query:
        person_list = Person.objects.filter(name__contains = search_query, )
    
        html = render_to_string('records/partial/top_search.html', {
            'person_list': person_list,
        })
    return JsonResponse(html, safe=False)


############################
# About US
############################
def aboutUS(request):
    check_session(request)
    return render(request, 'aboutUS.html')