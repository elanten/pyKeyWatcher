from django.contrib import admin

# Register your models here.

from .models import *


class ContactInfoInline(admin.TabularInline):
    model = ContactInfo
    extra = 1


class EmployeeGroupInline(admin.TabularInline):
    model = EmployeeGroup.members.through
    extra = 0


class EmployeeAdmin(admin.ModelAdmin):
    inlines = [
        ContactInfoInline,
        EmployeeGroupInline
    ]


admin.site.register(ContactType)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeGroup)
