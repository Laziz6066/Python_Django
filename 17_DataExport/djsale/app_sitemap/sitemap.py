from django.contrib.sitemaps import Sitemap
from app_sitemap.models import *
from django.urls import reverse


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return News.objects.all()

    def location(self, obj):
        return reverse('news-detail', args=[obj.pk])


class StaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['main_page', 'about_us', 'contacts']

    def location(self, item):
        return reverse(item)