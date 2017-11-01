# records/models.py
import csv
import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404

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
    name = models.CharField(max_length=50)
    nick_name = models.CharField(max_length=50, verbose_name='별칭', null=True, blank=True)
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

    # class Meta:
    #     ordering = ['name',]

    def __str__(self):
        return self.name

    @staticmethod
    def get_persons_following():
        pop_persons = {}
        count = 0
        persons = Person.objects.annotate(num_following=Count('following')).order_by('-num_following')
        for person in persons:
            pop_persons[person.name] = {}
            pop_persons[person.name]['id'] = person.id
            pop_persons[person.name]['name'] = person.name
            pop_persons[person.name]['following'] = person.num_following

            count += 1
            if count == 8:
                break
        return pop_persons

    @staticmethod
    def get_new_persons():
        new_persons = {}
        count = 0
        days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        persons = Person.objects.filter(created_date__gt = days_ago).annotate(
                num_following=Count('following')).order_by('-num_following')

        for person in persons:
            new_persons[person.name] = {}
            new_persons[person.name]['id'] = person.id
            new_persons[person.name]['name'] = person.name
            new_persons[person.name]['following'] = person.num_following

            count += 1
            if count == 8:
                break
        return new_persons


    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(',')
        for tag in tag_list:
            obj, created = Tag.objects.get_or_create(tag=tag.lower())
            self.tags.add(obj)

    def create_jobs(self, jobs):
        jobs = jobs.strip()
        job_list = jobs.split(',')
        for job in job_list:
            obj, created = Job.objects.get_or_create(name=job.lower())
            self.jobs.add(obj)

    def get_tags(self):
        return Tag.objects.filter(person=self)

    def get_tag3(self):
        return Tag.objects.filter(person=self)[:3]

    @property
    def total_likes(self):
        return self.user_like.count()

    @property
    def total_following(self):
        return self.following.count()   

    def get_parent(self):
        return [relation.other for relation in Relationship.objects.
            select_related("other").filter(person=self, relationship='parent')]
        # persons = Person.objects.filter(relationships__person=self, relationships__relationship='parent')
        # return persons

    def get_father(self):
        try:
            return [relation.other for relation in Relationship.objects.
                        select_related("other").filter(person=self, relationship='parent', ctype='아버지')][0]
        except Exception:
            return None

    def get_spouse(self):
        return [relation.other for relation in Relationship.objects.
            select_related("other").filter(person=self, relationship='spouse')]

    def get_children(self):
        return [relation.person for relation in Relationship.objects.select_related("person").
                filter(other=self, relationship='parent').order_by('person__sex', 'person__birth_year')]

    def get_sibling(self):
        try:
            father = self.get_father()
        except Exception as e:
            return None
        if father:
            return [relation.person for relation in Relationship.objects.select_related("person").
                filter(other=father, relationship='parent').order_by('-person__sex', 'person__birth_year')]
        else:
            return None

    def make_relationship(self, other, relationship, ctype, user):
        Relationship.objects.get_or_create(person=self, other=other, 
                relationship=relationship, ctype=ctype, created_user=user)

    # Get Nickname
    def get_nicknames(self):
        return PersonNick.objects.filter(person=self).annotate(
                num_userlike=Count('user_like')).order_by('-num_userlike')[:4]

    def get_total_nick(self):
        return PersonNick.objects.filter(person=self).annotate(
                num_userlike=Count('user_like')).count()

    def get_events(self):
        return PersonEvent.objects.filter(person=self).all()


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


from openpyxl import load_workbook
import pandas as pd
def read_person_data():

    User = get_user_model()
    user = User.objects.get(username='happy@naver.com')

    job_array = []
    wb = load_workbook('person.xlsx')
    ws = wb['Sheet']
    df = pd.DataFrame(ws.values)

    for index, row in df.iterrows():
        if index == 0:
            continue
        print(row)
        name = row[0]
        nick = row[1]
        birth = row[2]
        sex = row[3]
        jobs = row[4]
        tags = row[5]
        status = row[6]
        event = row[7]
        news = row[8]
        father = row[9]
        mother = row[10]
        spouse = row[11]
        url = row[12]
        picture = row[13]

        if isNumber(name):
            person = Person.objects.get(id=name)
        else:
            person, created = Person.objects.get_or_create(name=name, nick_name=nick, url=url,
                    birth_year=birth, sex=sex, status=status)
            print(person)
            # 사진 입력
            if picture:
                person.picture = picture
                person.save()

            person.create_tags(name)

            # Job 입력
            if jobs:
                person.create_jobs(jobs)

        if tags:
            person.create_tags(tags)

        # 뉴스와 이벤트 가져오기
        if event:
            event = get_object_or_404(Event, id=event)
            # PersonEvent 등록
            obj, created = PersonEvent.objects.get_or_create(person=person, 
                    event=event, created_user=user)
            if created:
                print('Event {} 와 사람 {} 이 생성되었습니다.'.format(event.name, person.name))
            else:
                print('{} 은 기존 사람입니다.'.format(person.name))

            if news:
                news = news.strip()
                new_list = news.split(',')
                for new in new_list:
                    if new:
                        news = get_object_or_404(News, id=new)
                        Evidence.objects.get_or_create(personevent=obj, news=news, created_user=user)

        if father:
            fathers = Person.objects.filter(name=father)
            if len(fathers) == 1:
                person.make_relationship(fathers[0], 'parent', '아버지', user)
            else:
                print("{} 가 동명이인입니다. 다시 입력하시기 바랍니다.".format(father))

        if mother:
            mothers = Person.objects.filter(name=mother)
            if len(mothers) == 1:
                person.make_relationship(mothers[0], 'parent', '어머니', user)
            else:
                print("{} 가 동명이인입니다. 다시 입력하시기 바랍니다.".format(mother))

        if spouse:
            spouses = Person.objects.filter(name=spouse)
            if len(spouses) == 1:
                if person.sex == 'M':
                    person.make_relationship(spouses[0], 'spouse', '아내', user)
                    spouses[0].make_relationship(person, 'spouse', '남편', user)
                else:
                    person.make_relationship(spouses[0], 'spouse', '남편', user)
                    spouses[0].make_relationship(person, 'spouse', '아내', user)
            else:
                print("{} 가 동명이인입니다. 다시 입력하시기 바랍니다.".format(mother))

class Relationship(models.Model):
    person = models.ForeignKey(Person, related_name='relationships')
    other = models.ForeignKey(Person, related_name='relationothers')
    relationship = models.CharField(max_length=10, 
        choices=(('spouse', 'spouse'),('parent', 'parent'),))
    ctype = models.CharField(max_length=10, 
        choices=(('아내', '아내'),('남편', '남편'),('아버지', '아버지'),('어머니', '어머니'),('아들', '아들'),('딸', '딸'),))
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

    @property
    def related_persons(self):
        return self.personevent_set.count()

    def person_list(self):
        return Person.objects.filter(personevent__event = self).annotate(
            num_following=Count('following')).filter(status='P').order_by('-num_following')

    def get_news(self):
        return News.objects.filter(events=self)
            

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
    events = models.ManyToManyField(Event, related_name='eventnews', blank=True)

    def __str__(self):
        return self.title

    def get_evidences(self):
        return Evidence.objects.filter(news=self)

    def get_comments(self):
        return self.comments.count()

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
        ordering = ('tag',)
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