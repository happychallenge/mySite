from django.contrib import admin

from .models import Comment, ENComment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment
    list_display = [ 'id', 'content', 'parent']


@admin.register(ENComment)
class ENCommentAdmin(admin.ModelAdmin):
    class Meta:
        model = ENComment
    list_display = ['id', 'event','news', 'content', 'parent']
