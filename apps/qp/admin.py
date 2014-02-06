from apps.qp.models import *
from django.contrib import admin


class BusinessAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('auth_user', 'name', 'logo','contact_person', 'contact_phone')
        }),
    )

class DocumentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('docfile', )
        }),
    )

class RaffleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('business', 'target_url', 'date_created', 'expiry_date')
        }),
    )

class TicketAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('raffle', 'owly_hash', 'activation_email', 'date_activated')
        }),
    )

admin.site.register(Business, BusinessAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Raffle, RaffleAdmin)
admin.site.register(Ticket, TicketAdmin)