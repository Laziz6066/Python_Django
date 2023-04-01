import datetime
from django.contrib.auth.views import LogoutView, LoginView
from django.views import View
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from .forms import NewsCommentForm, AuthForm
from .models import News, Comment, get_sentinel_user
from django import forms


class NewsCreationFormView(CreateView):
    model = News
    template_name = 'news/news_creation_page.html'
    fields = ['title', 'description']


class NewsEditFormView(UpdateView):
    model = News
    template_name = 'news/news_edit.html'
    fields = ['title', 'description', 'date_edit']
    initial = {'date_edit': datetime.datetime.now()}


class NewsListView(ListView):
    model = News
    ordering = ['-date_create']
    template_name = 'blog/news_list.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class NewsSinglePageView(DetailView):
    model = News
    template_name = 'news/news_single_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = self.object
        context['comments'] = self.object.comments.all()
        form = NewsCommentForm()

        if self.request.user.is_authenticated:
            form.fields['user_name'].widget = forms.HiddenInput()

        context['comment_form'] = form
        return context

    def post(self, request, **kwargs):
        news = self.get_object()
        comment_form = NewsCommentForm(request.POST)
        if comment_form.is_valid():
            if self.request.user.is_authenticated:
                news.activity += 1
                comment = comment_form.save(commit=False)
                comment.news_comment = news
                comment.user = request.user.username
                comment.user_name = request.user
                comment.save()
                news.save()
            else:
                news.activity += 1
                comment = comment_form.save(commit=False)
                comment.news_comment = news
                comment.save()
                news.save()
            return HttpResponseRedirect('/news_list')
        return render(request, 'news/news_single_page.html',
                      context={'comment_form': comment_form})


class LoginNewsView(LoginView):
    template_name = 'registration/login.html'


class LogoutNewsView(LogoutView):
    template_name = 'news/logout.html'