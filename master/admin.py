from django.contrib import admin
from master.models import Country, Region, Job, Media, EventCategory

# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    class Meta:
        model = Country
    list_display = ['id', 'ko_name', 'en_name']
    list_display_link = ['ko_name', 'en_name']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    class Meta:
        model = Region
    list_display = ['country', 'parent_region', 'region_name']
    list_display_link = ['country', 'parent_region', 'region_name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    class Meta:
        model = Job
    list_display = ['name']

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    class Meta:
        model = Media
    list_display = [ 'id', 'category', 'name', 'short']
    list_display_link = ['name']

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = EventCategory
    list_display = ['name']




