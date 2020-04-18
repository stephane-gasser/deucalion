from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User

class ContentPage(TimeStampedModel):
    author = models.ForeignKey(User, blank=True, null=True, default=None)
    title = models.CharField(max_length=100)
    site_url = models.CharField(max_length=250)
    original_location = models.CharField(max_length=250)
    content = models.TextField()
    short_description = models.TextField(blank=True)
    is_root = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.site_url

