# -*- coding: utf-8 -*-

from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from email_html.mail import send_mail

def send_confirmation_message_to_sender(message):
    subject = u"Message Deucalion n°%d - %s" % (
        message.discussion.id,
        message.discussion.subject,
        )
    template_name = "emails/Messages/first_message_confirmation.html"
    recipient = message.discussion.from_email
    message = render_to_string(
        template_name,
        {'site':Site.objects.get_current(), 'message':message})
    send_mail(subject, message, recipient_list=[recipient])

def notify_new_message(message):
    if message.discussion.message_set.count() == 1:
        send_confirmation_message_to_sender(message)
        
        subject = u"Mise en relation Deucalion n°%d - %s" % (
            message.discussion.id,
            message.discussion.subject,
            )
        template_name = "emails/Messages/new_discussion.html"
        recipient = message.discussion.to_user.email

    elif message.is_reply:
        subject = u"Réponse Deucalion n°%d - %s" % (
            message.discussion.id,
            message.discussion.subject,
            )
        template_name = "emails/Messages/new_message_reply.html"
        recipient = message.discussion.from_email

    else:
        subject = u"Réponse Deucalion n°%d - %s" % (
            message.discussion.id,
            message.discussion.subject,
            )
        template_name = "emails/Messages/new_message.html"
        recipient = message.discussion.to_user.email
    message = render_to_string(
        template_name,
        {'site':Site.objects.get_current(), 'message':message})
    send_mail(subject, message, recipient_list=[recipient])

def notify_change_of_status(discussion, custom_message):
    if discussion.status == "archived":
        subject = u"Déclinaison Deucalion n°%d - %s" % (
                discussion.id,
                discussion.subject,
                )
        template_name = "emails/Messages/declined.html"
        recipient = discussion.from_email
        message = render_to_string(
            template_name,
            {'site':Site.objects.get_current(), 'custom_message':custom_message})
        send_mail(subject, message, recipient_list=[recipient])

def notify_disclosure_request(discussion_disclosure):
    subject = u"Levée d'anonymat Deucalion n°%d - %s" % (
        discussion_disclosure.discussion.id,
        discussion_disclosure.discussion.subject,
        )
    template_name = "emails/Messages/disclosure_request.html"
    recipient = discussion_disclosure.discussion.from_email
    message = render_to_string(
        template_name,
        {'site':Site.objects.get_current(), 'discussion_disclosure':discussion_disclosure})
    send_mail(subject, message, recipient_list=[recipient])

def notify_disclosure_response(discussion_disclosure):
    subject = u"Levée d'anonymat Deucalion n°%d - %s" % (
        discussion_disclosure.discussion.id,
        discussion_disclosure.discussion.subject,
        )
    template_name = "emails/Messages/disclosure_response.html"
    recipient = discussion_disclosure.discussion.to_user.email
    message = render_to_string(
        template_name,
        {'site':Site.objects.get_current(), 'discussion_disclosure':discussion_disclosure})
    send_mail(subject, message, recipient_list=[recipient])


def notify_disclosure_refusal(discussion_disclosure):
    subject = u"Refus de levée d'anonymat Deucalion n°%d - %s" % (
        discussion_disclosure.discussion.id,
        discussion_disclosure.discussion.subject,
        )
    template_name = "emails/Messages/disclosure_refusal.html"
    recipient = discussion_disclosure.discussion.to_user.email
    message = render_to_string(
        template_name,
        {'site':Site.objects.get_current(), 'discussion_disclosure':discussion_disclosure})
    send_mail(subject, message, recipient_list=[recipient])

