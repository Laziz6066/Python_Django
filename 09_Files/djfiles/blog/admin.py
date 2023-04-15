from django.contrib import admin
from .models import *


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'description',)
    list_display_links = ('id', 'created_at', 'description',)


class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at',)


admin.site.register(BlogEntryModel, BlogEntryAdmin)
admin.site.register(FileModel, FileAdmin)