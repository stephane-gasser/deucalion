# -*- coding: utf-8 -*-
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

import hashlib, random

def _secret_hash():
    return hashlib.md5(str(random.random())).hexdigest()

def _secret_hash_reply():
    return hashlib.md5(str(random.random())).hexdigest()

class Discussion(TimeStampedModel):
    STATUS_CHOICES = (
        ('new', _(u'Nouveau')),
        ('active', _(u'En cours')),
        ('archived', _(u'Décliné')),
        ('contacted', _(u'Contacté')),
        )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="new")

    from_email = models.EmailField()
    from_user = models.ForeignKey(
        User, related_name="discussions_from",
        default=None, null=True, blank=True)
    to_user = models.ForeignKey(
        User, related_name="discussions_to")
    secret_hash = models.CharField(max_length=64, default=_secret_hash)
    secret_hash_reply = models.CharField(max_length=64, default=_secret_hash_reply)
    
    subject = models.CharField(max_length=250)

    def is_active(self):
        return self.status in ('new', 'active')
    def is_archived(self):
        return self.status in ('archived')
    def is_contacted(self):
        return self.status in ('contacted')

    def __unicode__(self):
        return self.subject

    @models.permalink
    def get_absolute_url(self):
        return ('Messages_discussion', (self.secret_hash,))

    @models.permalink
    def get_reply_url(self):
        return ('Messages_discussion_reply', (self.secret_hash_reply,))


    class Meta:
        ordering = ('created',)

class Message(TimeStampedModel):
    is_reply = models.BooleanField(default=False)
    discussion = models.ForeignKey(Discussion)
    message = models.TextField()

    class Meta:
        ordering = ('created',)

    def get_absolute_url(self):
        return self.discussion.get_absolute_url()+"#message-%d" % self.id

    def get_reply_url(self):
        return self.discussion.get_reply_url()+"#message-%d" % self.id

class DiscussionDisclosure(TimeStampedModel):
    discussion = models.OneToOneField(Discussion)

    STATUS_CHOICES = (
        ('none', _(u'Pas de demande')),
        ('sender_asked', _(u'Demande du prospect')),
        ('receiver_asked', _(u'Demande de l\'entreprise')),
        ('both_agreed', _(u'Contact partagé')),
        ('sender_declined', _(u'Refus du prospect')),
        ('receiver_declined', _(u'Refus de l\'entreprise')),
        )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="none")
    contact_email = models.EmailField(verbose_name=u"Email")
    contact_phone = models.CharField(verbose_name=u"Téléphone", max_length=50, blank=True)
    contact_name = models.CharField(verbose_name=u"Nom du contact", max_length=50, blank=True)
    contact_company = models.CharField(verbose_name=u"Entreprise", max_length=100, blank=True)
    contact_address = models.TextField(verbose_name=u"Adresse", max_length=100, blank=True)
    messages = models.TextField(blank=True)


    def is_open(self):
        return not "declined" in self.status and not "agreed" in self.status

    def is_refused(self):
        return "declined" in self.status
