from django.contrib import admin

from .models import AutoAddRequest, ManualAddRequest

admin.site.register(AutoAddRequest)
admin.site.register(ManualAddRequest)
