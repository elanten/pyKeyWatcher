from django.contrib import admin

# Register your models here.

from .models import DigitalKey, KeyType, KeyAllocation

admin.site.register(KeyType)
admin.site.register(KeyAllocation)
