from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Profile, BlogEntryModel, FileModel



class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='secret',
            city='New York',
            date_of_birth='1990-01-01',
            phone='1234567890',
            is_active=True,
        )

    def test_profile_attributes(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')
        self.assertEqual(self.profile.email, 'johndoe@example.com')
        self.assertEqual(self.profile.password, 'secret')
        self.assertEqual(self.profile.city, 'New York')
        self.assertEqual(str(self.profile.date_of_birth), '1990-01-01')
        self.assertEqual(self.profile.phone, '1234567890')
        self.assertTrue(self.profile.is_active)


class BlogEntryModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.blog_entry = BlogEntryModel.objects.create(
            description='Это тестовая запись в блоге',
            published='2022-02-23 00:00:00',
            author=self.user,
        )

    def test_blog_entry_attributes(self):
        self.assertEqual(self.blog_entry.description, 'Это тестовая запись в блоге')
        self.assertEqual(str(self.blog_entry.published), '2022-02-23 00:00:00')
        self.assertEqual(self.blog_entry.author, self.user)


