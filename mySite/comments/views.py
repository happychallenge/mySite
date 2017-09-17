from django.shortcuts import render
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

# from decorators import ajax_required
from .models import Comment
from .forms import CommentForm
# Create your views here.

@login_required
def comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        eid = request.POST.get('evidence')

        if form.is_valid():
            comment = form.save(commit=False)
            comment.created_user = request.user
            comment.save()

        comment_list = Comment.objects.filter(evidence__id = eid)
        return render(request, 'comments/partial/comment.html',
            { 'comment_list': comment_list, 'evidence_id': eid })

    else:
        eid = request.GET.get('evidence_id')
        comment_list = Comment.objects.filter(evidence__id = eid)
        return render(request, 'comments/partial/comment.html',
            { 'comment_list': comment_list, 'evidence_id': eid })