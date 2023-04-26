from market.forms import *
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from market.models import *
from django.test import TestCase


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