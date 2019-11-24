from django.contrib import admin
from preferences.admin import PreferencesAdmin
from .models import CoreAppSettings, Entry

admin.site.register(CoreAppSettings, PreferencesAdmin)
admin.site.register(Entry)