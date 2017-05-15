# records/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from master.models import Job, Region, EventCategory, Media
# Create your models here.
class Person(models.Model):
    """docstring for Person"""
    """ 기억할 인물에 대한 설명 """
    MALE = 'M'
    FEMALE = 'F'
    TYPE = (
        (MALE, '남'),
        (FEMALE, '여'),
    )

    DRAFT = 'D'
    PUBLISHED ='P'
    WITHDRAWN = 'W'
    STATUS_CHOICES = (
        (DRAFT, '초안'),
        (PUBLISHED, '공개'),
        (WITHDRAWN, '철회'),
    )
    name = models.CharField(max_length=30)
    nick_name = models.CharField(max_length=30, null=True, blank=True)
    birth = models.IntegerField(null=True, blank=True)
    jobs = models.ManyToManyField(Job, blank=True)
    picture = models.ImageField(null=True, blank=True)
    regions = models.ManyToManyField(Region, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    behavior = models.ManyToManyField('Event', through='PersonEvent',
                through_fields=('person', 'event'),)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_persons_published():
        persons = Person.objects.filter(status=Person.PUBLISHED).order_by('-id')
        return persons

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                tag, *_ = tag.split(',')
                t, created = Tag.objects.get_or_create(tag=tag.lower(),
                                    article=self)
    def get_tags(self):
        return Tag.objects.filter(article=self)


class Event(models.Model):
    """docstring for Event"""
    """ 설명 """
    name = models.CharField(max_length=30)
    content = models.TextField(null=True, blank=True)
    category = models.ForeignKey(EventCategory, null=True, blank=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
    happened_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PersonEvent(models.Model):
    """docstring for PersonBehavior"""
    """ 설명 """
    person = models.ForeignKey(Person, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    # news = models.ForeignKey('News', null=True, blank=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.person, self.event)

class News(models.Model):
    """docstring for News"""
    """ 설명 """
    media = models.ForeignKey(Media, null=True, blank=True)
    title = models.CharField(max_length=300)
    url = models.URLField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    published_at = models.DateField(null=True, blank=True)
    
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Evidence(models.Model):
    """docstring for Evidence"""
    """ Evidence """
    personevent = models.ForeignKey(PersonEvent)
    news = models.ForeignKey(News)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.personevent)


class Evaluation(models.Model):
    """docstring for Evaluation"""
    """ 설명 """
    personevent = models.ForeignKey(PersonEvent)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    score = models.IntegerField(default=0,
                validators=[MaxValueValidator(10), MinValueValidator(-10)])
    comment = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.score)


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.person_set.all()
        count = {}
        for tag in tags:
            if tag.tag in count:
                count[tag.tag] = count[tag.tag] + 1
            else:
                count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


