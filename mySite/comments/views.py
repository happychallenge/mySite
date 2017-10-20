from django.shortcuts import render
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# from decorators import ajax_required
from .models import Comment, ENComment
from .forms import CommentForm, ENCommentForm
# Create your views here.

def evidence_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        evidence = request.POST.get('evidence')

        if form.is_valid():
            user = request.user
            comment = form.save(commit=False)
            comment.created_user = user
            comment.save()

        comment_list = Comment.objects.filter(evidence__id = evidence, parent__isnull=True)
        return render(request, 'comments/partial/comment.html',
            { 'comment_list': comment_list, 'evidence_id': evidence })

    else:
        evidence = request.GET.get('evidence_id')
        comment_list = Comment.objects.filter(evidence__id = evidence, parent__isnull=True)
        return render(request, 'comments/partial/comment.html',
            { 'comment_list': comment_list, 'evidence_id': evidence })

def evi_comment_delete(request):
    comment_id = request.GET.get('comment')
    evidence = request.GET.get('evidence')

    Comment.objects.get(id=comment_id).delete()

    comment_list = Comment.objects.filter(evidence__id = evidence, parent__isnull=True)
    return render(request, 'comments/partial/comment.html',
        { 'comment_list': comment_list, 'evidence_id': evidence })

    

def news_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        newsid = request.POST.get('news')

        if form.is_valid():
            user = request.user
            comment = form.save(commit=False)
            comment.created_user = user
            comment.save()

        comment_list = Comment.objects.filter(evidence__id = eid)
        return render(request, 'comments/partial/comment.html',
            { 'comment_list': comment_list, 'evidence_id': eid })

    else:
        newsid = request.GET.get('news_id')
        eventid = request.GET.get('event_id')
        comment_list = Comment.objects.filter(event__id = eventid, news__id=newsid)
        return render(request, 'comments/partial/comment.html',
            { 'comment_list': comment_list, 'event_id': eventid, 'news_id': newsid })



