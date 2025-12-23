from django.contrib import admin
from django.contrib.admin import register
from page.models import Athnticate

@register(Athnticate)
class AthnticateAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'message']
    search_fields = ['name', 'email']
