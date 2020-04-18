# -*- coding: utf-8 -*-

from django.shortcuts import *
from django import http
from django.views.generic.edit import FormView
from django import forms
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.conf import settings

from main.Profiles.models import Profile
from .models import Discussion, Message, DiscussionDisclosure
from .utils import notify_new_message, notify_disclosure_request, notify_disclosure_response, notify_disclosure_refusal, notify_change_of_status

class NewDiscussionForm(forms.ModelForm):
    from_email = forms.EmailField(label="Votre adresse email", widget=forms.TextInput(attrs={'placeholder':'nom.prenom@exemple.com'}))
    subject = forms.CharField(label="Objet", widget=forms.TextInput(attrs={'placeholder':"De quoi s'agit-il ?"}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Décrivez votre besoin en quelques lignes'}))
    class Meta:
        model = Discussion
        fields = ('from_email', 'subject')

class NewDiscussionView(FormView):
    template_name = 'Messages/discussion_create.html'
    form_class = NewDiscussionForm

    def get_profile(self):
        return get_object_or_404(Profile, pk=self.kwargs.get('profile_pk'))

    def get_context_data(self, **kwargs):
        c = super(NewDiscussionView, self).get_context_data(**kwargs)
        c['object'] = self.get_profile()
        return c

    def get_initial(self):
        if self.request.COOKIES.has_key('from_email'):
            return {'from_email':self.request.COOKIES['from_email']}

    def form_valid(self, form):
        discussion = form.save(commit=False)
        discussion.to_user = self.get_profile().user
        if self.request.user.is_authenticated():
            discussion.from_user = self.request.user
        discussion.save()
        message = Message.objects.create(discussion=discussion, message=form.cleaned_data['message'])
        notify_new_message(message)
        response = http.HttpResponseRedirect(discussion.get_absolute_url())
        response.set_cookie('from_email', discussion.from_email)
        response.set_cookie('latest_discussion', discussion.secret_hash)
        return response

class NewMessageForm(forms.ModelForm):
    message = forms.CharField(
        label="Nouveau message",
        widget=forms.Textarea(attrs={'placeholder':'Votre réponse'}))
    class Meta:
        model = Message
        fields = ('message',)


class DiscussionDetail(FormView):
    template_name = "Messages/discussion_detail.html"
    form_class = NewMessageForm
    is_reply = False
    
    def get_discussion(self):
        return get_object_or_404(Discussion, secret_hash=self.kwargs['secret_hash'])
    
    def get_context_data(self, **kwargs):
        c = super(DiscussionDetail, self).get_context_data(**kwargs)
        discussion = self.get_discussion()
        c['object'] = discussion
        if self.request.user == discussion.to_user:
            c['is_recipient'] = True
        return c

    def form_valid(self, form):
        discussion = self.get_discussion()
        if not discussion.status == "active":
            discussion.status = "active"
            discussion.save()
        message = form.save(commit=False)
        message.discussion = discussion
        message.is_reply = self.is_reply
        message.save()
        notify_new_message(message)
        response = http.HttpResponseRedirect(discussion.get_absolute_url())
        response.set_cookie('latest_discussion', discussion.secret_hash)
        return response

    def get(self, *args, **kwargs):
        discussion = self.get_discussion()
        if self.request.user == discussion.to_user:
            return http.HttpResponseRedirect(discussion.get_reply_url())
        return super(DiscussionDetail, self).get(*args, **kwargs)


class DiscussionReplyDetail(DiscussionDetail):
    is_reply = True

    def get_context_data(self, **kwargs):
        c = super(DiscussionReplyDetail, self).get_context_data(**kwargs)
        c['disclosure_cost'] = settings.DISCLOSURE_COST
        c['credits'] = self.request.user.get_profile().credits
        return c

    def get_discussion(self):
        return get_object_or_404(Discussion, secret_hash_reply=self.kwargs['secret_hash'])

    def get(self, *args, **kwargs):
        discussion = self.get_discussion()
        if not self.request.user == discussion.to_user:
            return redirect_to_login(discussion.get_reply_url(), reverse('login'))
        return super(DiscussionDetail, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        discussion = self.get_discussion()
        if not self.request.user == discussion.to_user:
            return http.HttpResponseForbidden()
        return super(DiscussionDetail, self).post(*args, **kwargs)

class DiscussionSetStatusView(DiscussionReplyDetail):
    def post(self, *args, **kwargs):
        discussion = self.get_discussion()
        if not self.request.user == discussion.to_user:
            return http.HttpResponseForbidden()
        discussion.status = self.kwargs['status']
        discussion.save()
        notify_change_of_status(discussion, self.request.POST.get('message'))
        return http.HttpResponseRedirect(discussion.get_reply_url())

    def get_template_names(self):
        if self.kwargs['status'] == "archived": ## aka decline
            return 'Messages/discussion_decline.html'
        return super(DiscussionSetStatusView, self).get_template_name()

    def get_form_class(self):
        if self.kwargs['status'] == "archived": ## aka decline
            class DeclineForm(forms.Form):
                message = forms.CharField(label="Message personnalisé",
                                          widget=forms.Textarea(attrs={'placeholder':'Veuillez motiver votre décision'}))
            return DeclineForm
        return super(DiscussionSetStatusView, self).get_form_class()
        

class DiscussionListView(ListView):
    def get_context_data(self, **kwargs):
        c = super(DiscussionListView, self).get_context_data(**kwargs)
        c['type'] = self.request.GET.get('type', 'active')
        return c

    def get_queryset(self):
        t = self.request.GET.get('type', 'active')
        if t=="all":    
            return self.request.user.discussions_to.all()
        elif t=="archived":
            return self.request.user.discussions_to.filter(status="archived")
        elif t=="contacted":
            return self.request.user.discussions_to.filter(status="contacted")
        else:
            return self.request.user.discussions_to.filter(status__in=('new', 'active'))

class DiscussionDisclosureResponseForm(forms.ModelForm):
    ## message = forms.CharField(
    ##     label="Message",
    ##     widget=forms.Textarea(attrs={'placeholder':'Votre message personnalisé'}))
    class Meta:
        model = DiscussionDisclosure
        fields = ('contact_email', 'contact_phone', 'contact_name', 'contact_company', 'contact_address')

class DiscussionDisclosureRefuseForm(forms.ModelForm):
    class Meta:
        model = DiscussionDisclosure
        fields = ()

class DiscussionDisclosureRequest(DiscussionReplyDetail):
    template_name = "Messages/discussion_disclosure_request.html"

    def post(self, request, **kwargs):
        discussion = self.get_discussion()
        discussion_disclosure = DiscussionDisclosure.objects.create(
            contact_email = discussion.from_email,
            discussion = discussion,
            status = "receiver_asked")
        notify_disclosure_request(discussion_disclosure)
        response = http.HttpResponseRedirect(discussion.get_reply_url())
        response.set_cookie('latest_discussion', discussion.secret_hash)        
        return response

class DiscussionDisclosureResponse(DiscussionDetail):
    template_name = "Messages/discussion_disclosure_response.html"
    form_class = DiscussionDisclosureResponseForm

    def form_valid(self, form):
        discussion = self.get_discussion()
        
        if self.request.user == discussion.to_user:
            return http.HttpResponseForbidden()

        profile = discussion.to_user.get_profile()

        self.proceed(form, discussion, profile)

        return http.HttpResponseRedirect(discussion.get_absolute_url())

    def get_form_kwargs(self):
        kwargs = super(DiscussionDisclosureResponse, self).get_form_kwargs()
        kwargs.update({
            'instance':self.get_discussion().discussiondisclosure
            })
        return kwargs

class DiscussionDisclosureAgree(DiscussionDisclosureResponse):
    def proceed(self, form, discussion, profile):
        if not profile.credits >= settings.DISCLOSURE_COST:
            logging.warning(u'Insufficient fundings for %s', profile)

        discussion_disclosure = form.save(commit=False)
        discussion_disclosure.status = "both_agreed"
        discussion_disclosure.save()
        discussion.status = "contacted"
        discussion.save()

        profile.add_credits(-settings.DISCLOSURE_COST, comment=u"Levée d'anonymat avec %s" % discussion_disclosure.contact_email)

        notify_disclosure_response(discussion_disclosure)
        

class DiscussionDisclosureRefuse(DiscussionDisclosureResponse):
    template_name = "Messages/discussion_disclosure_refuse.html"
    form_class = DiscussionDisclosureRefuseForm

    def proceed(self, form, discussion, profile):
        discussion_disclosure = form.save(commit=False)
        discussion_disclosure.status = "sender_declined"
        discussion_disclosure.save()

        notify_disclosure_refusal(discussion_disclosure)
