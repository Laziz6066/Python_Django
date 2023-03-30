from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *


class Home(ListView):
    model = Ads
    template_name = 'advertisements_app/home_list.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'The python'
        return context


class Detail(DetailView):
    model = Ads
    template_name = 'advertisements_app/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        item = super().get_object(queryset)
        item.incrementViewCount()
        return item
