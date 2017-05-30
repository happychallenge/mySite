# records/views.py
from django.shortcuts import render, get_object_or_404
from .models import Person, PersonEvent, Event

# Create your views here.
def person_list(request):
    person_list = Person.objects.prefetch_related('tags', 'jobs').all()
    context = {'person_list': person_list}
    return render(request, 'records/person_list.html', context)


def person_detail(request, person_id):
    person = Person.objects.prefetch_related('tags', 'jobs').get(id=person_id)
    personevent_list = PersonEvent.objects.select_related('event', 'person').filter(person=person).all()
    context = { 'person': person, 'personevent_list': personevent_list }
    return render(request, 'records/person_detail.html', context)


def event_detail(request, event_id):
    event = Event.objects.select_related('category').get(id=event_id)
    personevent_list = PersonEvent.objects.select_related('person').filter(event=event).all()
    context = { 'event': event, 'personevent_list': personevent_list }
    return render(request, 'records/event_detail.html', context)