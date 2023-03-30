from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


admin.site.register(Ads)
admin.site.register(Author)
admin.site.register(Category)