from django.shortcuts import *
from django.template import RequestContext

def default(request):
    return render_to_response("default.html", RequestContext(request))
