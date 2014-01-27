from apps.qp.models import *
from django.contrib import admin


class BusinessAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('auth_user', 'name', 'contact_person', 'contact_phone')
        }),
    )


admin.site.register(Business, BusinessAdmin)