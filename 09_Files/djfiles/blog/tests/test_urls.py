from blog.views import *
from django.test import SimpleTestCase
from django.urls import reverse, resolve



class TestUrls(SimpleTestCase):

    def test_blog_url_resolves(self):
        url = reverse('blog')
        self.assertEqual(resolve(url).func.view_class, BlogListView)

    def test_entry_url_resolves(self):
        url = reverse('blog_entry')
        self.assertEqual(resolve(url).func.view_class, BlogEntryView)

    def test_detail_url_resolves(self):
        url = reverse('detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, BlogDetail)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, AppLogin)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutNewsView)

    def test_register_url_resolves(self):
        url = reverse('another_register')
        self.assertEqual(resolve(url).func.view_class, AnotherRegisterView)

    def test_accounts_url_resolves(self):
        url = reverse('acc')
        self.assertEqual(resolve(url).func.view_class, Accounts)

    def test_edit_profile_url_resolves(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func.view_class, EditProfileView)

    def test_upload_files_url_resolves(self):
        url = reverse('upload_files', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UploadFilesView)

    def test_upload_csv_url_resolves(self):
        url = reverse('upload_csv')
        self.assertEqual(resolve(url).func.view_class, UpdateCsvView)

