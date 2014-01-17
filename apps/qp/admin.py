from apps.qp.models import Business
from django.contrib import admin
from django.contrib.admin import ModelAdmin

class BusinessAdmin(ModelAdmin):
        pass
admin.site.register(Business, BusinessAdmin)
