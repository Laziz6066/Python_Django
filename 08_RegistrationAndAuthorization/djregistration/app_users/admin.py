from django.contrib import admin
from .models import *


class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag']


admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Tag, TagAdmin)