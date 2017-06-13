from django.contrib import admin

# Register your models here.

from .models import DigitalKey, KeyType, KeyAssignment

admin.site.register(KeyType)
admin.site.register(KeyAssignment)
