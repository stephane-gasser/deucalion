from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Profile, Company

from .views import CreditLineView

urlpatterns = patterns('',
    url('^(?P<pk>\d+)/$',
      DetailView.as_view(model=Profile),
      name="Profile_detail"),
    url('^credits/$',
      login_required(CreditLineView.as_view()),
      name="Profile_credit_line")
      )
