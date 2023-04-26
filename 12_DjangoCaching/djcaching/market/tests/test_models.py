from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from market.models import *
from django.utils import timezone



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


class BalanceModelTest(TestCase):

    def setUp(self):
        self.profile = Profile.objects.create(
            name='John Doe',
            email='johndoe@example.com',
            phone='555-555-5555'
        )
        self.balance = Balance.objects.create(
            profile=self.profile,
            balance=100.00
        )

    def test_balance_profile_is_one_to_one(self):
        field_type = type(self.balance.profile)
        expected_type = type(self.profile)
        self.assertEqual(field_type, expected_type)

    def test_balance_default_value_is_zero(self):
        balance = Balance.objects.create(profile=self.profile)
        self.assertEqual(balance.balance, 0)

    def test_balance_string_representation(self):
        expected = f'{self.balance.profile} - Balance: ${self.balance.balance}'
        self.assertEqual(str(self.balance), expected)


class ShopsModelTest(TestCase):

    def setUp(self):
        self.shop = Shops.objects.create(
            shop_name='Test Shop'
        )

    def test_shop_name_max_length(self):

        max_length = self.shop._meta.get_field('shop_name').max_length
        self.assertEqual(max_length, 15)

    def test_shop_created_at_auto_now_add(self):
        created_at = self.shop.created_at
        now = timezone.now()
        self.assertAlmostEqual(created_at, now, delta=timezone.timedelta(seconds=1))

    def test_shop_string_representation(self):
        expected = f'{self.shop.shop_name}'
        self.assertEqual(str(self.shop), expected)


class ItemsModelTest(TestCase):

    def setUp(self):
        self.shop = Shops.objects.create(
            shop_name='Test Shop'
        )
        self.item = Items.objects.create(
            shop=self.shop,
            item_name='Test Item',
            stocks='10 available',
            offers='Buy one get one free',
            price=10.99
        )

    def test_item_shop_is_foreign_key(self):

        field_type = type(self.item.shop)
        expected_type = type(self.shop)
        self.assertEqual(field_type, expected_type)

    def test_item_stocks_can_be_blank(self):

        item = Items.objects.create(
            shop=self.shop,
            item_name='Test Item 2',
            price=5.99
        )
        self.assertIsNone(item.stocks)

    def test_item_offers_can_be_blank(self):

        item = Items.objects.create(
            shop=self.shop,
            item_name='Test Item 3',
            price=15.99
        )
        self.assertIsNone(item.offers)

    def test_item_price_has_max_digits_and_decimal_places(self):

        max_digits = self.item._meta.get_field('price').max_digits
        decimal_places = self.item._meta.get_field('price').decimal_places
        self.assertEqual(max_digits, 10)
        self.assertEqual(decimal_places, 2)

    def test_item_created_at_auto_now_add(self):

        created_at = self.item.created_at
        self.assertIsNotNone(created_at)

    def test_item_string_representation(self):

        expected = f'{self.item.item_name} - Price: ${self.item.price}'
        self.assertEqual(str(self.item), expected)



class PurchaseModelTest(TestCase):

    def setUp(self):
        self.shop = Shops.objects.create(
            shop_name='Test Shop'
        )
        self.item = Items.objects.create(
            shop=self.shop,
            item_name='Test Item',
            price=10.99
        )
        self.balance = Balance.objects.create(
            profile_id=1,
            balance=50.00
        )
        self.purchase = Purchase.objects.create(
            item=self.item,
            balance=self.balance
        )

    def test_purchase_item_is_foreign_key(self):

        field_type = type(self.purchase.item)
        expected_type = type(self.item)
        self.assertEqual(field_type, expected_type)

    def test_purchase_balance_is_foreign_key(self):

        field_type = type(self.purchase.balance)
        expected_type = type(self.balance)
        self.assertEqual(field_type, expected_type)

    def test_purchase_timestamp_auto_now_add(self):

        timestamp = self.purchase.timestamp
        self.assertIsNotNone(timestamp)

    def test_purchase_string_representation(self):

        expected = f'{self.item.item_name} - ${self.item.price} - {self.balance.profile_id}'
        self.assertEqual(str(self.purchase), expected)