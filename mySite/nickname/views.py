from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Nickname
from mySite.records.models import PersonNick, Person


@login_required
def add_like_nick(request):
    data = dict()
    user = request.user

    nickname_id = request.GET.get('nickname_id')
    personnick = get_object_or_404(PersonNick, id=nickname_id)
    user_hate_list = personnick.user_hate.all()
    if user in user_hate_list:
        data['is_valid'] = False
        data['messages'] = '이미 싫어한다를 선택하셨습니다. 같은 항목에 대해 두가지 선택은 불가능합니다.'
        return JsonResponse(data)

    user_like_list = personnick.user_like.all()
    if user in user_like_list:
        data['is_valid'] = False
        data['messages'] = '이미 좋아한다고 선택하셨습니다.'
    else:
        data['is_valid'] = True;
        personnick.user_like.add(user)
        data['total_likes'] = personnick.total_likes
    return JsonResponse(data)

@login_required
def add_hate_nick(request):
    data = dict()
    user = request.user

    nickname_id = request.GET.get('nickname_id')
    personnick = get_object_or_404(PersonNick, id=nickname_id)
    user_like_list = personnick.user_like.all()
    if user in user_like_list:
        data['is_valid'] = False
        data['messages'] = '이미 좋아한다를 선택하셨습니다. 같은 항목에 대해 두가지 선택은 불가능합니다.'
        return JsonResponse(data)

    user_hate_list = personnick.user_hate.all()
    if user in user_hate_list:
        data['is_valid'] = False
        data['messages'] = '이미 싫어한다를 선택하셨습니다.'
    else:
        data['is_valid'] = True;
        personnick.user_hate.add(user)
        data['total_hates'] = personnick.total_hates
    return JsonResponse(data)

############################
# Search Nickname
############################
@login_required
def search_nicknames(request):
    search_query = request.GET.get('keyword')
    if search_query:
        nickname_list = Nickname.objects.filter(nickname__contains=search_query)
        
        html = render_to_string('nickname/partial/search_nickname.html', {
            'nickname_list': nickname_list,
        })
        
        return JsonResponse(html, safe=False)

@login_required
def add_nickname(request, person_id):
    if request.method == "POST":
        person = get_object_or_404(Person, id=person_id)
        nickname_id = request.POST.get("nickname_id")

        if nickname_id:
            nickname = get_object_or_404(Nickname, id=nickname_id)
            PersonNick.objects.get_or_create(
                    person=person, nickname=nickname, created_user=request.user)

        else:
            nickname = request.POST.get("nickname")
            if nickname:
                obj, created = Nickname.objects.get_or_create(nickname=nickname)
                PersonNick.objects.get_or_create(
                    person=person, nickname=obj, created_user=request.user)

    personnick_list = PersonNick.objects.filter(person=person).annotate(
                num_userlike=Count('user_like')).order_by('-num_userlike')
    return render(request, 'nickname/partial/nicknames.html', {'personnick_list':personnick_list})


@login_required
def get_all_nickname(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    
    personnick_list = PersonNick.objects.filter(person=person).annotate(
                num_userlike=Count('user_like')).order_by('-num_userlike')
    return render(request, 'nickname/partial/nicknames.html', {'personnick_list':personnick_list})




