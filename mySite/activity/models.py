from django.db import models
from django.conf import settings
from django.utils.html import escape

from mySite.records.models import Person, Event, Evidence

# Create your models here.
class Notification(models.Model):
    LIKED = 'PL'
    COMMENTED = 'PC'
    FOLLOWING = 'PF'

    ANSWERED = 'A'
    ACCEPTED_ANSWER = 'W'
    EDITED_ARTICLE = 'E'
    ALSO_COMMENTED = 'S'
    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (FOLLOWING, 'FOLLOWING'),

        (ANSWERED, 'Answered'),
        (ACCEPTED_ANSWER, 'Accepted Answer'),
        (EDITED_ARTICLE, 'Edited Article'),
        (ALSO_COMMENTED, 'Also Commented'),
    )

    _LIKED_TEMPLATE = '<a href="/{0}/">{1}</a> liked your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> commented on your post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501
    _FOLLOWING_TEMPLATE = '<a href="/{0}/">{1}</a> favorited your question: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _ANSWERED_TEMPLATE = '<a href="/{0}/">{1}</a> answered your question: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _ACCEPTED_ANSWER_TEMPLATE = '<a href="/{0}/">{1}</a> accepted your answer: <a href="/questions/{2}/">{3}</a>'  # noqa: E501
    _EDITED_ARTICLE_TEMPLATE = '<a href="/{0}/">{1}</a> edited your article: <a href="/article/{2}/">{3}</a>'  # noqa: E501
    _ALSO_COMMENTED_TEMPLATE = '<a href="/{0}/">{1}</a> also commentend on the post: <a href="/feeds/{2}/">{3}</a>'  # noqa: E501

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    created_date = models.DateTimeField(auto_now_add=True)
    person = models.ForeignKey(Person, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    evidence = models.ForeignKey(Evidence, null=True, blank=True)
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-created_date',)

    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                self.person.pk,
                escape(self.person.name)
                )
        elif self.notification_type == self.COMMENTED:
            return self._COMMENTED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                self.person.pk,
                escape(self.person.name)
                )
        elif self.notification_type == self.FOLLOWING:
            return self._FOLLOWING_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                self.person.pk,
                escape(self.person.name)
                )
        # elif self.notification_type == self.ANSWERED:
        #     return self._ANSWERED_TEMPLATE.format(
        #         escape(self.from_user.username),
        #         escape(self.from_user.first_name),
        #         self.question.pk,
        #         escape(self.get_summary(self.question.title))
        #         )
        # elif self.notification_type == self.ACCEPTED_ANSWER:
        #     return self._ACCEPTED_ANSWER_TEMPLATE.format(
        #         escape(self.from_user.username),
        #         escape(self.from_user.first_name),
        #         self.answer.question.pk,
        #         escape(self.get_summary(self.answer.description))
        #         )
        # elif self.notification_type == self.EDITED_ARTICLE:
        #     return self._EDITED_ARTICLE_TEMPLATE.format(
        #         escape(self.from_user.username),
        #         escape(self.from_user.first_name),
        #         self.article.slug,
        #         escape(self.get_summary(self.article.title))
        #         )
        # elif self.notification_type == self.ALSO_COMMENTED:
        #     return self._ALSO_COMMENTED_TEMPLATE.format(
        #         escape(self.from_user.username),
        #         escape(self.from_user.first_name),
        #         self.feed.pk,
        #         escape(self.get_summary(self.feed.post))
        #         )
        else:
            return 'Ooops! Something went wrong.'

