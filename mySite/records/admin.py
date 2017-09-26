# records/admin.py
from django.contrib import admin
from .models import Person, Tag, Event, PersonEvent, Relationship
from .models import News, Evaluation, Evidence
# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    class Meta:
        model = Person
    list_display = ['id', 'name', 'nick_name', 'birth_year', 'sex', 'picture', 'status']
    list_editable = ['sex', 'nick_name', 'birth_year', 'status']
    search_fields = ['name']


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    class Meta:
        model = Relationship
    list_display = ['person', 'other', 'relationship', 'ctype']
    list_editable = [ 'ctype' ]
    search_fields = ['person__name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    class Meta:
        model = Event
    list_display = [ 'id', 'name', 'category', 'get_tags']

    def get_tags(self, obj):
        return ", ".join([tag.tag for tag in obj.tags.all()])

@admin.register(PersonEvent)
class PersonEventAdmin(admin.ModelAdmin):
    class Meta:
        model = PersonEvent

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    class Meta:
        model = News
    list_display = ['media', 'title', 'created_user']

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    class Meta:
        model = Evidence
    list_display = [ 'id', 'personevent', 'news']

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    class Meta:
        model = Evaluation
    list_display = ['personevent', 'user', 'score', 'created_at']

