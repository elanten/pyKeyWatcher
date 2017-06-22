from django.contrib import admin

# Register your models here.
from key_manual.models import *


admin.site.register(ManualType)
admin.site.register(ManualTag)
admin.site.register(Manual)
