from django.db import models
from django.conf import settings

from mySite.records.models import Evidence

# Create your models here.
class Comment(models.Model):
    """docstring for Comment"""
    """ 설명 """
    evidence = models.ForeignKey(Evidence, related_name='comments', null=True, blank=True)
    parent = models.ForeignKey("self", related_name='children', null=True, blank=True)
    content = models.TextField()
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ( 'id', )

    def __str__(self):
        return "{} {}".format(self.evidence, self.created_user)

    def as_tree(self):
        children = list(sf.children.all())
        branch = bool(children)
        yield branch, self
        for child in children:
            for next in child.as_tree():
                yield next
        yield branch, None
