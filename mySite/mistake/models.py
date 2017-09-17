from django.db import models

# Create your models here.
class Report(models.Model):
    """docstring for Report"""
    """ Report of Mistake """
    name = models.CharField(max_length=30, verbose_name='오류 명칭')
    url = models.URLField(null=True, blank=True, verbose_name='뉴스 등록이 안 되는 URL')
    content = models.TextField(null=True, blank=True)
    picture = models.ImageField( upload_to='error_report/%Y/%m/', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
