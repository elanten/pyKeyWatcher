from django.contrib import admin

# Register your models here.
from digital_key.models import WorkSystem
from .models import DigitalKey, KeyType, KeyAssignment


class DigitalKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial', 'date_expire')
    list_filter = ['date_expire']


admin.site.register(KeyType)
admin.site.register(KeyAssignment)
admin.site.register(WorkSystem)
admin.site.register(DigitalKey, DigitalKeyAdmin)
