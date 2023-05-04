from django.contrib.syndication.views import Feed
from django.db.models import QuerySet
from django.urls import reverse
from app_sitemap.models import *


class LatestHouseFedd(Feed):
    name = 'Дом'
    link = '/sitehouse/'
    description = 'Жильё'

    def items(self) -> QuerySet:
        return Housing.objects.order_by('-name')

    def item_title(self, item: Housing) -> str:
        return item.name

    def item_description(self, item: Housing) -> str:
        return item.description

    def item_link(self, item: Housing) -> str:
        return reverse('house-item', args=[item.pk])