from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn',)
    list_display_links = ('id', 'title', 'isbn',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)