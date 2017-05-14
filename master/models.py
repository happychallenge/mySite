from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
import csv


class Country(models.Model):
    """docstring for Country"""
    """ 설명 """
    ko_name     = models.CharField(max_length=30, verbose_name='국가명')
    en_name     = models.CharField(max_length=30, verbose_name='English Name')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ko_name

class Region(models.Model):
    """docstring for Region"""
    """ 행정구역 """
    country = models.ForeignKey(Country)
    parent_region = models.ForeignKey('Region', null=True, blank=True)
    region_name     = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        if self.parent_region is None:
            return "{}".format(self.region_name)
        else:
            return "{} {}".format(self.parent_region, self.region_name)

def read_region_data():
    with open('korea_city.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        country = Country.objects.get(id=1)

        for row in reader:
            large = row.get('large')
            middle = row.get('middle')
            small = row.get('small')

            reg, created = Region.objects.get_or_create(country=country, region_name=large)
            print(reg, created)
            reg, created = Region.objects.get_or_create(country=country, parent_region=reg, region_name=middle)
            print(reg, created)
            if small:
                reg, created = Region.objects.get_or_create(country=country, parent_region=reg, region_name=small)

# Create your models here.
class Job(models.Model):
    """docstring for Job"""
    """ 설명 """
    name    = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

MEDIA_CATEGORY = (
    ('TV', 'TV'),
    ('신문', '신문'),
    ('인터넷', '인터넷'),
)

# 매체 구분
class Media(models.Model):
    """docstring for Media"""
    """ Media """
    name    = models.CharField(max_length=30)
    short    = models.CharField(max_length=30)
    category = models.CharField(max_length=10, choices=MEDIA_CATEGORY)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


def read_media():
    with open('Media.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        for row in reader:
            name = row.get('Name')
            short = row.get('Short')
            category = row.get('Category')
            print(name, short, category)
            reg, created = Media.objects.get_or_create(name=name, short=short, category=category)


class EventCategory(models.Model):
    """docstring for EventCategory"""
    """ 설명 """
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

