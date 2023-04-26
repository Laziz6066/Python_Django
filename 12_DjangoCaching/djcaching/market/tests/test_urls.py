from django.test import SimpleTestCase
from django.urls import reverse, resolve
from market.views import *

class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, ShopListView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, AppLogin)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, LogoutNewsView)

    def test_register_url_resolves(self):
        url = reverse('another_register')
        self.assertEquals(resolve(url).func.view_class, AnotherRegisterView)

    def test_account_url_resolves(self):
        url = reverse('account')
        self.assertEquals(resolve(url).func.view_class, AccountView)

    def test_replenish_balance_url_resolves(self):
        url = reverse('top_up_your_balance', args=[1])
        self.assertEquals(resolve(url).func.view_class, ReplenishBalanceView)

    def test_shop_detail_url_resolves(self):
        url = reverse('detail', args=[1])
        self.assertEquals(resolve(url).func.view_class, ShopDetailView)

    def test_buy_item_url_resolves(self):
        url = reverse('buy_item', args=[1])
        self.assertEquals(resolve(url).func.view_class, BuyItemView)

    def test_history_url_resolves(self):
        url = reverse('history')
        self.assertEquals(resolve(url).func.view_class, HistoryView)