from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.
from mySite.activity.models import Notification


class Profile(models.Model):
    """docstring for Profile"""
    """ 설명 """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    picture = models.ImageField(upload_to='user_profile/%Y/%m/', 
                    verbose_name='', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # 성적 (등록 글, 커멘트 등에 점수를 부여함)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def notify_person_liked(self, person):
        if self.user != person.created_user:
            Notification(notification_type=Notification.LIKED, 
                from_user=self.user, to_user=person.created_user,
                person=person).save()

    def notify_person_unliked(self, person):
        if self.user != person.created_user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                from_user=self.user, to_user=person.created_user,person=person).delete()

    def notify_person_commented(self, person):
        if self.user != person.created_user:
            Notification(notification_type=Notification.COMMENTED, 
                from_user=self.user, to_user=person.created_user,
                person=person).save()

    def notify_person_following(self, person):
        if self.user != person.created_user:
            Notification(notification_type=Notification.FOLLOWING, 
                from_user=self.user, to_user=person.created_user,
                person=person).save()

    def notify_person_unfollowing(self, person):
        if self.user != person.created_user:
            Notification.objects.filter(notification_type=Notification.FOLLOWING,
                from_user=self.user, to_user=person.created_user,person=person).delete()

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(save_user_profile, sender=settings.AUTH_USER_MODEL)