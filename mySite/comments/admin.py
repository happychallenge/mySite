from django.contrib import admin

from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment
    list_display = [ 'id', 'created_user', 'evidence', 'content', 'parent']
