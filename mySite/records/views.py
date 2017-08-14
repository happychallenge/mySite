# records/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import get_user_model

from .models import Person, PersonEvent, Event, Tag

# Create your views here.

def _person_list(request, person_list):
    paginator = Paginator(person_list, 6)
    page = request.GET.get('page')

    try:
        person_list = paginator.page(page)
    except PageNotAnInteger:
        person_list = paginator.page(1)
    except EmptyPage:
        person_list = paginator.page(paginator.num_pages)
    
    popular_tags = Tag.get_person_popular_tags()
    context = {'person_list': person_list, 'popular_tags': popular_tags}
    return render(request, 'records/person_list.html', context)

def person_list(request):
    person_list = Person.objects.prefetch_related('tags', 'jobs').all()
    return _person_list(request, person_list)


def person_detail(request, person_id):
    person = Person.objects.select_related('created_user').prefetch_related(
            'tags', 'jobs', 'personevent_set__event', 'personevent_set__evidence_set__news', 
            'user_like', 'following').get(id=person_id)
    # personevent_list = PersonEvent.objects.select_related('event', 'person').filter(person=person).all()
    context = { 'person': person, }
    return render(request, 'records/person_detail.html', context)


# Create your views here.
def _event_list(request, event_list):
    event_list = event_list.order_by()
    paginator = Paginator(event_list, 6)
    page = request.GET.get('page')

    try:
        event_list = paginator.page(page)
    except PageNotAnInteger:
        event_list = paginator.page(1)
    except EmptyPage:
        event_list = paginator.page(paginator.num_pages)
    
    popular_tags = Tag.get_event_popular_tags()    
    context = {'event_list': event_list, 'popular_tags': popular_tags}
    return render(request, 'records/event_list.html', context)

def event_list(request):
    event_list = Event.objects.prefetch_related('tags', 'user_like', 
            'following').select_related('category', 'created_user').all()
    return _event_list(request, event_list)


def event_detail(request, event_id):
    event = Event.objects.select_related('category').get(id=event_id)
    personevent_list = PersonEvent.objects.select_related('person').filter(event=event).all()
    context = { 'event': event, 'personevent_list': personevent_list }
    return render(request, 'records/event_detail.html', context)


############################
# Person
############################
@login_required
@require_http_methods(["POST"])
def ajax_person_like(request, person_id):
    data = dict()
    # person_id = request.POST.get('personid')
    person = get_object_or_404(Person, id=person_id)
    user_list = person.user_like.all()
    
    if request.user in user_list :
        person.user_like.remove(request.user)
        data['like'] = 'like'
    else:
        person.user_like.add(request.user)
        data['like'] = 'unlike'

    data['status'] = True
    data['total_likes'] = person.total_likes

    return JsonResponse(data)    


@login_required
@require_http_methods(["POST"])
def ajax_person_following(request, person_id):
    data = dict()
    
    person = get_object_or_404(Person, id=person_id)
    user_list = person.following.all()
    
    if request.user in user_list :
        person.following.remove(request.user)
        data['follow'] = 'following'
        data['message'] = '{} 님 지켜 보기을 취소하셨습니다.'.format(person.name)
    else:
        person.following.add(request.user)
        data['follow'] = 'unfollowing'
        data['message'] = '{} 님 지켜 보기가 신청되었습니다.'.format(person.name)

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
        data['message'] = '사건 "{}" 지켜 보기가 신청되었습니다.'.format(event.name)

    data['status'] = True
    data['total_following'] = event.total_following

    return JsonResponse(data)    

############################
# Tag
############################
@login_required
def tag(request, tag_name, type):
    tag = Tag.objects.get(tag=tag_name)
    if type == 'P':
        person_list = tag.person_set.all() 
        return _person_list(request, person_list)
    else:
        event_list = tag.event_set.all() 
        return _event_list(request, event_list)