from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from .forms import *
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime, csv
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from PIL import Image
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    model = BlogEntryModel
    context_object_name = 'files'
    ordering = ['-created_at']


class BlogEntryView(LoginRequiredMixin, CreateView):
    model = BlogEntryModel
    template_name = 'blog/blog_entry.html'
    fields = ['description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogDetail(DetailView):
    model = BlogEntryModel
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = self.object
        return context


class AnotherRegisterView(FormView):
    template_name = 'blog/another_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('blog')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        Profile.objects.create(
            user=user,
            city=form.cleaned_data['city'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            phone=form.cleaned_data['phone']
        )
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})



class AppLogin(LoginView):
    template_name = 'blog/login.html'


class LogoutNewsView(LogoutView):
    template_name = 'blog/logout.html'


class Accounts(ListView):
    model = Profile
    template_name = 'blog/about_me.html'
    context_object_name = 'acc'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'blog/edit_profile.html'
    success_url = reverse_lazy('acc')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.save()
        return response


class UploadFilesView(FormView):
    template_name = 'blog/upload_files.html'
    form_class = MultiFileForm

    def get_success_url(self):
        return reverse('blog')

    def form_valid(self, form):
        blog_entry = get_object_or_404(BlogEntryModel, pk=self.kwargs['pk'])
        files = self.request.FILES.getlist('file_field')
        for f in files:
            instance = FileModel(file=f, download=blog_entry)
            instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog_entry'] = get_object_or_404(BlogEntryModel, pk=self.kwargs['pk'])
        return context





class UpdateCsvView(UpdateView):
    template_name = 'blog/update_csv.html'
    model = BlogEntryModel
    form_class = CsvUploadForm
    success_url = reverse_lazy('blog')

    def form_valid(self, form):
        file = form.cleaned_data['file']
        file_content = file.read().decode('utf-8')
        reader = csv.reader(file_content.splitlines())
        headers = next(reader)

        with transaction.atomic():
            for row in reader:
                blog = self.get_object()
                blog.description = row[0]
                blog.published = row[1]
                blog.save()

        messages.success(self.request, 'CSV file uploaded successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error uploading CSV file.')
        return super().form_invalid(form)
