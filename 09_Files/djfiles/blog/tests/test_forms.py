from django.test import TestCase
from blog.forms import *
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import *


class TestAuthForm(TestCase):

    def test_auth_valid_form(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        form = AuthForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'testuser')
        self.assertEqual(form.cleaned_data['password'], 'testpass')


class TestRegisterForm(TestCase):

    def test_register_valid_form(self):
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'DjangoModule9',
            'password2': 'DjangoModule9',
            'date_of_birth': '2000-01-01',
            'city': 'Test City',
            'phone': '1234567890'
        }
        form = RegisterForm(data=form_data)

        self.assertTrue(form.is_valid(), form.errors.as_text())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'testuser@example.com')


class TestEditProfileForm(TestCase):

    def test_edit_profile_valid_form(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe'
        }
        form = EditProfileForm(data=form_data, instance=user)

        self.assertTrue(form.is_valid())
        form.save()
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')


        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog_entry = BlogEntryModel.objects.create(description='Test description', author=self.user)


class TestFileForms(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog_entry = BlogEntryModel.objects.create(description='Test description', author=self.user)

    def test_file_valid_form(self):
        form_data = {
            'description': 'Описание тестового файла',
            'file': SimpleUploadedFile('test_file.txt', b'Содержимое тестового файла'),
        }
        form = FileForms(data=form_data)
        self.assertTrue(form.is_valid())

        file_obj = form.save(commit=False)
        file_obj.download = self.blog_entry
        file_obj.save()

        self.assertTrue(FileModel.objects.filter(file='photo/test_file.txt').exists())
        self.assertEqual(file_obj.description, 'Описание тестового файла')


class TestMultiFileForm(TestCase):

    def test_miltifile_valid_form(self):
        form_data = {}
        file_data = [
            SimpleUploadedFile('test_file1.txt', b'Содержимое тестового файла 1'),
            SimpleUploadedFile('test_file2.txt', b'Содержимое тестового файла 2')
        ]
        form = MultiFileForm(data=form_data, files={'file_field': file_data})

        self.assertTrue(form.is_valid())
        for uploaded_file in form.cleaned_data['file_field']:
            self.assertTrue(uploaded_file.size > 0)


class TestCsvUploadForm(TestCase):

    def test_csv_upload_valid_form(self):

        csv_data = "name,age\nAlice,25\nBob,30\n"
        csv_file = SimpleUploadedFile('test_file.csv', csv_data.encode())
        form_data = {'file': csv_file}
        form = CsvUploadForm(data=form_data, files=form_data)


        self.assertTrue(form.is_valid())
        file_contents = form.cleaned_data['file'].read().decode()
        self.assertEqual(file_contents, csv_data)