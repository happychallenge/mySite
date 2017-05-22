from django.contrib import admin
from .models import Profile

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = Profile
    list_display = [ 'user', 'image']
