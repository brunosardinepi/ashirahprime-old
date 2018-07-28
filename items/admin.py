from django.contrib import admin

from . import models


class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user')

admin.site.register(models.Item, ItemAdmin)