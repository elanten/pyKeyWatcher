from django.contrib import admin

# Register your models here.

from .models import DigitalKey, KeyType

admin.site.register(KeyType)
# admin.site.register(DigitalKey)
