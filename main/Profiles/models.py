from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from wymeditor.models import WYMEditorField


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    website = models.URLField(blank=True)
    presentation = WYMEditorField(blank=True)
    picture = models.ImageField(
        upload_to='companies/',
        blank=True, null=True, default=None)

    class Meta:
        verbose_name_plural = "Companies"

    def __unicode__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User)
    company = models.ForeignKey(
        Company, null=True, blank=True, default=None)
    role = models.CharField(max_length=100)
    picture = models.ImageField(
        upload_to='profiles/',
        blank=True, null=True, default=None)
    bio = WYMEditorField(blank=True)
    phone = models.CharField(max_length=100, blank=True)

    credits = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s" % (self.user.get_full_name().strip() or self.user.username)

    @models.permalink
    def get_absolute_url(self):
        return ('Profile_detail', (self.pk,))

    def add_credits(self, inc, comment=None):
        self.credits += inc
        self.creditline_set.create(credits=self.credits, comment=comment)
        self.save()

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        try:
            latest_credits = self.creditline_set.latest().credits
        except:
            latest_credits = 0
        if not latest_credits == self.credits:
            self.creditline_set.create(credits=self.credits)

class CreditLine(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile)
    credits = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True, default=None)

    class Meta:
        ordering = ("-timestamp", )
        get_latest_by = "timestamp"
