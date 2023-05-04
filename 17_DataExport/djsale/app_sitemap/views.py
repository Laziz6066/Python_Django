from django.shortcuts import render
from .models import *
from django.views.generic import View, ListView, DetailView


def main_page(request):
    return render(request, 'app_sitemap/main_page.html')


class House(ListView):
    model = Housing
    template_name = 'app_sitemap/list_of_housing_for-sale.html'
    context_object_name = 'house'


def about_us(request):
    return render(request, 'app_sitemap/about_us.html')


def contacts(request):
    return render(request, 'app_sitemap/contacts.html')


class News(ListView):
    model = News
    template_name = 'app_sitemap/news.html'
    context_object_name = 'news'


class NewsDetail(DetailView):
    model = News
    template_name = 'app_sitemap/news.html'
    context_object_name = 'news'