# records/views.py
from django.shortcuts import render, get_object_or_404
from .models import Person, PersonEvent

# Create your views here.
def people_list(request):
    people_list = Person.objects.prefetch_related('tags', 'jobs').all()
    context = {'people_list': people_list}
    return render(request, 'records/people_list.html', context)

def people_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    personevent_list = PersonEvent.objects.select_related('event').filter(person=person).all()
    context = { 'person': person, 'personevent_list': personevent_list }
    return render(request, 'records/people_detail.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    personevent_list = PersonEvent.objects.select_related('person').filter(event=event).all()
    context = { 'event': event, 'personevent_list': personevent_list }
    return render(request, 'records/event_detail.html', context)