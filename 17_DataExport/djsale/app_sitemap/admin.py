from django.contrib import admin
from .models import *


class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)


class TypeOfRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_room',)
    list_display_links = ('id', 'type_room',)


class NumberOfRoomsAdmin(admin.ModelAdmin):
    list_display = ('id', 'numbers_room',)
    list_display_links = ('id', 'numbers_room',)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_display_links = ('id', 'title',)


admin.site.register(Housing, HouseAdmin)
admin.site.register(TypeOfRoom, TypeOfRoomAdmin)
admin.site.register(NumberOfRooms, NumberOfRoomsAdmin)
admin.site.register(News, NewsAdmin)
