#!/usr/bin/python
import os
import sys

from os.path import abspath, dirname, join
from site import addsitedir
FCGI_ROOT = sys.path[0] ## real dirname of this script (thanx to mod_fcgi ?) this is needed on alwaysdata, because django.fcgi is a symlink and dirname/abspath do not work apparently
PROJECT_ROOT = join(FCGI_ROOT, "../")
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, join(PROJECT_ROOT, "deploy/site-packages/"))
sys.path.insert(0, join(PROJECT_ROOT, "apps"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "../"))
sys.path.insert(0, join(PROJECT_ROOT, "external/"))

from django.conf import settings
os.environ["DJANGO_SETTINGS_MODULE"] = "main.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
