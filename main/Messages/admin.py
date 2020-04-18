from django.contrib import admin

from .models import Discussion, Message, DiscussionDisclosure

class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'from_email', 'from_user', 'to_user', 'created')
    date_hierarchy = 'created'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'is_reply', 'created')
    date_hierarchy = 'created'

admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(DiscussionDisclosure)
