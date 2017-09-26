from django.contrib import admin

from .models import Nickname
from mySite.records.models import PersonNick

# Register your models here.
@admin.register(Nickname)
class NicknameAdmin(admin.ModelAdmin):
    class Meta:
        model = Nickname
    list_display = ['nickname', ]


@admin.register(PersonNick)
class PersonNickAdmin(admin.ModelAdmin):
    class Meta:
        model = PersonNick
    list_display = ['person', 'nickname',]
