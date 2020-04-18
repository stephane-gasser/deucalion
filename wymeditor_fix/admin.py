from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.forms import FlatpageForm

from wymeditor.widgets import WYMEditorArea

admin.site.unregister(FlatPage)

class WYMFlatpageForm(FlatpageForm):
    class Meta(FlatpageForm.Meta):
        widgets = {
            'content':WYMEditorArea
            }

class WYMFlatPageAdmin(FlatPageAdmin):
    form = WYMFlatpageForm

admin.site.register(FlatPage, WYMFlatPageAdmin)
