from django.contrib import admin
from .models import *


class ShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at',)
    list_display_links = ('id', 'created_at',)


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name',)
    list_display_links = ('id', 'item_name',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name',)
    list_display_links = ('first_name', 'id',)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Shops, ShopsAdmin)
admin.site.register(Items, ItemsAdmin)