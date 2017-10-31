from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from mySite.records.models import Event

# Create your views here.
@login_required
def event_list(request):
    today = date.today()
    year = today.year
    from_dt = today + timedelta(days=-90)
    to_dt = today + timedelta(days=90)

    event_list = {}
    events = Event.objects.filter(happened_at__isnull=False)
    times = [ time for time in range(10, 23)]
    # print(times)
    for event in events:
        event_list[event.id] = {}
        event_list[event.id]['id'] = event.id
        event_list[event.id]['name'] = event.name
        hdate = event.happened_at.replace(year=year)
        # print(hdate)
        event_list[event.id]['hdate'] = hdate

    print(event_list)

    return render(request, 'calendars/event_list.html', {
            'event_list':event_list,
            'times':times,
        })
