from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .views import *


urlpatterns = patterns('',
                       url('^new/(?P<profile_pk>\d+)/$', NewDiscussionView.as_view(), name='Messages_new_discussion'),
                       url('^list/$', login_required(DiscussionListView.as_view()), name='Messages_list'),
                       url('^(?P<secret_hash>[a-z0-9]+)/$', DiscussionDetail.as_view(), name='Messages_discussion'),
                       url('^(?P<secret_hash>[a-z0-9]+)/reply/$', DiscussionReplyDetail.as_view(), name='Messages_discussion_reply'),
                       url('^(?P<secret_hash>[a-z0-9]+)/set/(?P<status>\w+)/$', DiscussionSetStatusView.as_view(), name='Messages_discussion_set_status'),
                       url('^(?P<secret_hash>[a-z0-9]+)/disclose/$', DiscussionDisclosureRequest.as_view(), name='Messages_discussion_disclosure_request'),
                       url('^(?P<secret_hash>[a-z0-9]+)/disclose/agree/$', DiscussionDisclosureAgree.as_view(), name='Messages_discussion_disclosure_agree'),
                       url('^(?P<secret_hash>[a-z0-9]+)/disclose/refuse/$', DiscussionDisclosureRefuse.as_view(), name='Messages_discussion_disclosure_refuse'),
                       )
