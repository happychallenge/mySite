from django.shortcuts import render

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

    

def en_comment(request):
    if request.method == 'POST':
        form = ENCommentForm(request.POST)
        eventid = request.POST.get('event')
        newsid = request.POST.get('news')

        if form.is_valid():
            user = request.user
            comment = form.save(commit=False)
            comment.created_user = user
            comment.save()

        comment_list = ENComment.objects.filter(
                event__id = eventid, news__id = newsid, parent__isnull=True)
        return render(request, 'comments/partial/en_comment.html',
            { 'comment_list': comment_list, 'evidence_id': eventid })

    else:
        newsid = request.GET.get('news')
        eventid = request.GET.get('event')
        comment_list = ENComment.objects.filter(
                event__id = eventid, news__id = newsid, parent__isnull=True)
        return render(request, 'comments/partial/en_comment.html',
            { 'comment_list': comment_list, 'event_id': eventid, 'news_id': newsid })


def en_comment_delete(request):
    comment_id = request.GET.get('comment')
    event = request.GET.get('event')
    newsid = request.GET.get('news')

    ENComment.objects.get(id=comment_id).delete()

    comment_list = ENComment.objects.filter(
        event__id = event, news__id = newsid, parent__isnull=True)
    return render(request, 'comments/partial/en_comment.html',
        { 'comment_list': comment_list, 'event_id': event, 'news_id': newsid })

