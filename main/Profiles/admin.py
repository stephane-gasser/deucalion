from django.contrib import admin

from .models import Company, Profile, CreditLine

from wymeditor.admin import WYMAdmin

admin.site.register(Company, WYMAdmin)

class ProfileAdmin(WYMAdmin):
    list_display = ('user', 'company', 'role', 'credits')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'company__name', 'company__location', 'role')

admin.site.register(Profile, ProfileAdmin)

class CreditLineAdmin(admin.ModelAdmin):
    list_display = ("profile", "timestamp", "credits", "comment")

admin.site.register(CreditLine, CreditLineAdmin)
