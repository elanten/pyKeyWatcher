from django.contrib import admin

# Register your models here.

from .models import ContactType

admin.site.register(ContactType)