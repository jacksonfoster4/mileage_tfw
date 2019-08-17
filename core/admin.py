from django.contrib import admin
from preferences.admin import PreferencesAdmin
from .models import CoreAppSettings

admin.site.register(CoreAppSettings, PreferencesAdmin)