# records/models.py
import csv
from django.db import models
from django.db.models import Count
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from mySite.master.models import Job, Region, EventCategory, Media
from mySite.nickname.models import Nickname

# Create your models here.


class Person(models.Model):
    """docstring for Person"""
    """ 기억할 인물에 대한 설명 """
    MALE = 'M'
    FEMALE = 'F'
    SEX = (
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
    nick_name = models.CharField(max_length=30, verbose_name='별칭', null=True, blank=True)
    birth_year = models.IntegerField(null=True, verbose_name='출생년도', blank=True)
    sex = models.CharField(max_length=1, choices=SEX, default=MALE)
    jobs = models.ManyToManyField(Job, blank=True)
    picture = models.ImageField(upload_to='person_picture/%Y/%m/', null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    regions = models.ManyToManyField(Region, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='person_liked', blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='person_follow', blank=True)
    created_date = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name

    @staticmethod
    def get_persons_following():
        persons = Person.objects.annotate(num_following=Count('following')).order_by('-num_following')
        return persons

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(',')
        for tag in tag_list:
            if tag:
                obj, created = Tag.objects.get_or_create(tag=tag.lower())
                self.tags.add(obj)
                
    def get_tags(self):
        return Tag.objects.filter(person=self)

    @property
    def total_likes(self):
        return self.user_like.count()

    @property
    def total_following(self):
        return self.following.count()        

    def get_parent(self):
        return [relation.other for relation in Relationship.objects.select_related("other").filter(person=self, relationship='parent')]

    def get_spouse(self):
        return [relation.other for relation in Relationship.objects.select_related("other").filter(person=self, relationship='spouse')]

    def get_children(self):
        return [relation.person for relation in 
            Relationship.objects.select_related("person").filter(other=self, relationship='parent').order_by('person__sex', 'person__birth_year')]

    def get_sibling(self):
        try:
            father = [relation.other for relation in Relationship.objects.select_related("other").filter(
                person=self, relationship='parent', ctype='아버지')][0]
        except Exception as e:
            return None
        if father:
            return [relation.person for relation in Relationship.objects.select_related("person").filter(
                other=father, relationship='parent').order_by('person__sex', 'person__birth_year')]
        else:
            return None

    # Get Nickname
    def get_nicknames(self):
        return PersonNick.objects.filter(person=self).annotate(
                num_userlike=Count('user_like')).order_by('-num_userlike')[:4]

    def get_total_nick(self):
        return PersonNick.objects.filter(person=self).annotate(
                num_userlike=Count('user_like')).count()

def read_person_data():
    
    job_array = []
    with open('/Users/happy/Django/mySite/mySite/records/person.csv', "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print('TEST')
        print(reader)

        for row in reader:
            print("TEST 2")
            name = row.get('name')
            nick = row.get('nick')
            birth = row.get('birth')
            sex = row.get('sex')
            jobs = row.get('jobs')
            # url = row.get('url')
            tags = row.get('tags')
            status = row.get('status')

            person, created = Person.objects.get_or_create(name=name, nick_name=nick, 
                        birth_year=birth, sex=sex, status=status)

            print(person)
            person.create_tags(tags)
            person.create_tags(name)

            if jobs:
                jobed, created = Job.objects.get_or_create(name=jobs)
                    
                person.jobs.add(jobed)


class Relationship(models.Model):
    person = models.ForeignKey(Person, related_name='relationships')
    other = models.ForeignKey(Person, related_name='relationothers')
    relationship = models.CharField(max_length=10, 
        choices=(('spouse', 'spouse'),('parent', 'parent'),))
    ctype = models.CharField(max_length=10, 
        choices=(('결혼', '결혼'),('이혼', '이혼'),('아버지', '아버지'),('어머니', '어머니'),('아들', '아들'),('딸', '딸'),))
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    
    class Meta:
        unique_together = (('person', 'other'), ('other', 'person'), )

    def __str__(self):
        return "{} is {} of {}".format(self.other, self.relationship, self.person)


class Event(models.Model):
    """docstring for Event"""
    """ 설명 """
    name = models.CharField(max_length=30)
    content = models.TextField(null=True, blank=True)
    category = models.ForeignKey(EventCategory, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_liked', blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='event_follow', blank=True)
    happened_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def total_likes(self):
        return self.user_like.count()

    @property
    def total_following(self):
        return self.following.count()   

class PersonEvent(models.Model):
    """docstring for PersonBehavior"""
    """ 설명 """
    person = models.ForeignKey(Person, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("person", "event"),)

    def __str__(self):
        return '{} {}'.format(self.person, self.event)

class News(models.Model):
    """docstring for News"""
    """ 설명 """
    media = models.ForeignKey(Media, null=True, blank=True)
    title = models.CharField(max_length=300)
    url = models.URLField(unique=True)
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

    class Meta:
        unique_together = (("personevent", "news"),)

    def __str__(self):
        return '{} {}'.format(self.personevent, self.news)


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
    tag = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag

    @staticmethod
    def get_person_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            count[tag.tag] = tag.person_set.count()
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:10]

    @staticmethod
    def get_event_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            count[tag.tag] = tag.event_set.count()
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:10]


class PersonNick(models.Model):
    """docstring for PersonNick"""
    """ 설명 """
    person = models.ForeignKey(Person)
    nickname = models.ForeignKey(Nickname)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='nickname_liked', blank=True)
    user_hate = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='nickname_hated', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('person', 'nickname'),)

    def __str__(self):
        return "{} {}".format(self.person, self.nickname)

    @staticmethod
    def get_user_like():
        personnicks = PersonNick.objects.annotate(num_userlike=Count('user_like')).order_by('-num_userlike')
        return personnicks

    @property
    def total_likes(self):
        return self.user_like.count()

    @property
    def total_hates(self):
        return self.user_hate.count()