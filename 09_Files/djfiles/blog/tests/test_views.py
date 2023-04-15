from django.test import TestCase, Client
from django.urls import reverse
from blog.models import *
import json
from django.contrib.auth.models import User
from datetime import datetime
from datetime import date
from django.shortcuts import redirect
from django.core.files.uploadedfile import SimpleUploadedFile



class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.blog_url = reverse('blog')
        self.author = User.objects.create_user(username='testuser', password='testpass')
        self.blog_entry = BlogEntryModel.objects.create(
            description='Test blog content',
            created_at=datetime.now(),
            published=datetime.now(),
            author=self.author
        )
        self.detail_url = reverse('detail', kwargs={'pk': self.blog_entry.pk})
        self.acc_url = reverse('acc')


    def test_blog_list_GET(self):
        response = self.client.get(self.blog_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_blog_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')

    def test_accaunts_list_GET(self):
        response = self.client.get(self.acc_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about_me.html')


class TestAnotherRegisterView(TestCase):
    def test_register_form_submission(self):
        url = reverse('another_register')
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'date_of_birth': '1990-01-01',
            'city': 'Test City',
            'phone': '555-1234',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class EditProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('edit_profile')
        self.data = {'first_name': 'John', 'last_name': 'Doe'}

    def test_edit_profile(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('acc'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')


class UploadFilesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.blog_entry = BlogEntryModel.objects.create(
            description='Test Blog Entry',
            author=self.user
        )

    def test_upload_files(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('upload_files', kwargs={'pk': self.blog_entry.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/upload_files.html')

        file_contents = b'Содержимое тестового файла'
        file = SimpleUploadedFile('test.txt', file_contents)

        data = {'file_field': [file]}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog'))

        file_model = FileModel.objects.filter(download=self.blog_entry).first()
        self.assertIsNotNone(file_model)
        self.assertEqual(file_model.file.read(), file_contents)