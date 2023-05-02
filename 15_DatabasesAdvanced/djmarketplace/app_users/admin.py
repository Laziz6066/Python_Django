from django.contrib import admin
from .models import *



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name',)
    list_display_links = ('first_name', 'id',)



class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance',)
    list_display_links = ('id', 'balance',)



# class StatusAdmin(admin.ModelAdmin):
#     list_display = ('id', 'status',)
#     list_display_links = ('id', 'status',)


class ShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at',)
    list_display_links = ('id', 'created_at',)


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name',)
    list_display_links = ('id', 'item_name',)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance',)
    list_display_links = ('id', )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Shops, ShopsAdmin)
admin.site.register(Items, ItemsAdmin)
# admin.site.register(Status, StatusAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Balance, BalanceAdmin)