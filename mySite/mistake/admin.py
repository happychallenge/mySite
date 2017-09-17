from django.contrib import admin

from .models import Report
# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    class Meta:
        model = Report
    list_display = ['name', 'url', 'email']
