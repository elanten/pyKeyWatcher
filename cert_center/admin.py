from django.contrib import admin
from .models import *

# Register your models here.


# class CertRequirementInline(admin.TabularInline):
#     model = CertRequirement
#     extra = 1
#
#
# class CertificationCenterAdmin(admin.ModelAdmin):
#     inlines = [CertRequirementInline]


admin.site.register(CertificationCenter)
admin.site.register(CertRequirement)
