from django.contrib import admin

from . import models


class GuildAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_public',)
    filter_horizontal = ('members',)

admin.site.register(models.Guild, GuildAdmin)