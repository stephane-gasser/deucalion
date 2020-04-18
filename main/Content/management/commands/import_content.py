from django.core.management.base import BaseCommand, CommandError
import BeautifulSoup

import os, glob, urllib
import re

import logging

def doit(path):
    from django.contrib.auth.models import User
    from main.Content.models import ContentPage

    def parse_page(f):
        soup = BeautifulSoup.BeautifulSoup(open(f), fromEncoding="utf8")
        def _get_meta(soup, name):
            tags = soup('meta', attrs={'name':name})
            if tags: return tags[-1]['content']
        def _get_title(soup):
            tags = soup('title') + soup('h1') ## fault taulerance
            for tag in tags:
                if tag.string: return tag.string

        title = _get_title(soup)
        author_username = _get_meta(soup, "author")
        site_url = "/" + _get_meta(soup, "siteurl")

        if author_username:
            author, _created = User.objects.get_or_create(username=author_username)
        else:
            author = None

        return {
            'title':title,
            'author':author,
            'site_url':site_url,
            'soup':soup
            }

    def _get_content(bag, soup):
        for link in soup('a'):
            if bag.has_key(link['href']):
                link['href'] = bag[link['href']]['site_url']
        return "".join(map(unicode, soup.body))
        
    bag = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            file_path = os.path.join(root, f)
            bag[f] = parse_page(file_path)

    for f, data in bag.items():
        page, _created = ContentPage.objects.get_or_create(original_location=f)
        page.title = data['title']
        page.author = data['author']
        page.site_url = data['site_url']
        page.content = _get_content(bag, data['soup'])
        page.is_root = (f == "index.html")
        try:
            page.save()
        except Exception, e:
            logging.error(u'Problem with %s: %s', f, e)

class Command(BaseCommand):
    args = 'directory'
    help = 'Import content data from html files ; index.html is expected in imported directory as root document. This can take some time.'

    def handle(self, *args, **options):
        for path in args:
            doit(path)
