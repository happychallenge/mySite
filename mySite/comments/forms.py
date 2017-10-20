from django import forms

from .models import Comment, ENComment

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['evidence', 'parent', 'content']

class ENCommentForm(forms.ModelForm):

    class Meta:
        model = ENComment
        fields = ['event', 'news', 'parent', 'content']
