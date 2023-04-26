from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from market.models import *
from market.forms import *


class ShopListViewTestCase(TestCase):
    def setUp(self):
        self.shop = Shops.objects.create(shop_name='Test Shop', description='This is a test shop')
        self.client = Client()

    def test_shop_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/list_of_stores.html')
        self.assertContains(response, self.shop.shop_name)


class ShopDetailViewTestCase(TestCase):
    def setUp(self):
        self.shop = Shops.objects.create(shop_name='Test Shop', description='This is a test shop')
        self.item = Items.objects.create(shop=self.shop, item_name='Test Item', description='This is a test item', price=Decimal('10.0'))
        self.client = Client()

    def test_shop_detail_view(self):
        response = self.client.get(reverse('detail', kwargs={'pk': self.shop.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/market_detail.html')
        self.assertContains(response, self.shop.shop_name)
        self.assertContains(response, self.item.item_name)
        self.assertContains(response, self.item.price)


class AnotherRegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'city': 'Test City',
            'date_of_birth': '2000-01-01',
            'phone': '+1234567890'
        }

    def test_another_register_view(self):
        response = self.client.post(reverse('another_register'), data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.city, self.data['city'])
        self.assertEqual(profile.phone, self.data['phone'])
        self.assertEqual(profile.date_of_birth, self.data['date_of_birth'])
        self.assertEqual(profile.first_name, self.data['first_name'])
        self.assertEqual(profile.last_name, self.data['last_name'])
        self.assertEqual(profile.email, self.data['email'])


class AppLoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()

    def test_app_login_view(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class LogoutNewsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'market/logout.html')


class AccountViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user)
        self.shop = Shops.objects.create(shop_name='Test Shop')
        self.item = Items.objects.create(item_name='Test Item', shop=self.shop, price=10)
        self.client.login(username='testuser', password='12345')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/market/account/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('account'))
        self.assertTemplateUsed(response, 'market/account.html')

    def test_view_context_contains_profile(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.context['profile'], self.profile)

    def test_view_context_contains_shop(self):
        response = self.client.get(reverse('account'))
        self.assertQuerysetEqual(response.context['shop'], [repr(self.shop)])

    def test_view_context_contains_item(self):
        response = self.client.get(reverse('account'))
        self.assertQuerysetEqual(response.context['item'], [repr(self.item)])

    def tearDown(self):
        self.client.logout()