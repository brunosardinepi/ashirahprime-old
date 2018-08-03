from django.contrib import admin

from . import models


class MailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'sender', 'recipient', 'subject',)

admin.site.register(models.Message, MailAdmin)