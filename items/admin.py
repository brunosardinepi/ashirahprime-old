from django.contrib import admin

from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'owner')

admin.site.register(models.Item, ItemAdmin)