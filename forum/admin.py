from django.contrib import admin

from . import models


class ForumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'date', 'title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'date',)

admin.site.register(models.Forum, ForumAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)