from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.utils import timezone



class NewsView(ListView):
    model = News
    template_name = 'blog/news_list.html'
    ordering = ['-created_at']
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['selected_tag'] = self.request.GET.get('tag')
        return context

    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__tag=tag)
        return queryset



def another_register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            date_of_birth = form.cleaned_data.get('date_of_birth')
            city = form.cleaned_data.get('city')
            phone = form.cleaned_data.get('phone')
            user.save()
            Profile.objects.create(
                user=user,
                city=city,
                date_of_birth=date_of_birth,
                phone=phone,

            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/blog')
    else:
        form = RegisterForm()
    return render(request, 'blog/another_register.html', {'form': form})


class DetailViewNews(DetailView):
    model = News
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = self.object
        context['comments'] = self.object.comments.all()
        form_class = NewsCommentForm()

        context['comment_form'] = form_class
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
            return HttpResponseRedirect('/blog')
        return render(request, 'blog/detail.html',
                      context={'comment_form': comment_form})





class NewsCreationView(CreateView):
    model = News
    template_name = 'blog/create_news.html'
    fields = ['title', 'description', 'tags']



# class NewsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
#     model = News
#     template_name = 'blog/news_edit.html'
#     fields = ['title', 'description']
#
#
#     def get_object(self, queryset=None):
#         obj = UpdateView.get_object(self, queryset=None)
#         if not obj.author == self.request.user:
#             redirect(reverse_lazy("blog"))
#         return obj


class AppLogin(LoginView):
    template_name = 'blog/login.html'




class LogoutNewsView(LogoutView):
    template_name = 'blog/logout.html'


class Accounts(ListView):
    model = Profile
    template_name = 'blog/about_me.html'
    context_object_name = 'acc'


class ModeratorViews(ListView):
    model = News
    template_name = 'blog/post.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.objects.filter(is_published=False)


class ModDetail(PermissionRequiredMixin, DetailView, UpdateView):
    model = News
    template_name = 'blog/mod_post_detail.html'
    form_class = ModerForm
    permission_required = 'blog.can_publish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = self.object
        return context


class ModUserViews(ListView):
    model = User
    template_name = 'blog/users.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return User.objects.filter(is_active=False)



class UserDetailView(PermissionRequiredMixin, DetailView, UpdateView):
    model = User
    template_name = 'blog/users_detail.html'
    form_class = ModerUserForm
    permission_required = 'blog.can_publish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = self.object
        return context
