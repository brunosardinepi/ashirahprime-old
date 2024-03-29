from django.contrib import admin

from . import models


class CharacterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user')

admin.site.register(models.Character, CharacterAdmin)