from django.shortcuts import *
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from django import http

from .models import ContentPage

class ContentIndexView(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        root_pages = ContentPage.objects.filter(is_root=True)
        if not root_pages.count():
            return "/"
        return root_pages[0].get_absolute_url()
    
class ContentPageView(DetailView):
    def get_object(self):
        page = get_object_or_404(ContentPage, site_url="/"+self.kwargs['site_url'])
        return page
