from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from datetime import date
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver


logger = logging.getLogger(__name__)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    first_name = models.CharField(max_length=35, verbose_name=_('first_name'))
    last_name = models.CharField(max_length=35, verbose_name=_('last_name'))
    email = models.EmailField(max_length=35, verbose_name=_('email'))
    password = models.CharField(max_length=35, verbose_name=_('password'))
    city = models.CharField(max_length=35, blank=True, verbose_name=_('city'))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_('date_of_birth'))
    phone = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('phone'))
    is_active = models.BooleanField(default=False, verbose_name=_('is_active'))
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('total_spent'))
    status = models.PositiveIntegerField(default=5, verbose_name=_('status'))

    def save(self, *args, **kwargs):
        if self.total_spent > 600:
            self.status = 4
        if self.total_spent > 2000:
            self.status = 3
        if self.total_spent > 6000:
            self.status = 2
        if self.total_spent > 10000:
            self.status = 1
        if self.status == 0:
            self.status += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('top_up_your_balance', args=[str(self.id)])

    def __str__(self):
        return self.first_name


class Balance(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, verbose_name=_('profile'))
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('balance'))

    def __str__(self):
        return f'{self.profile} - {self.balance}'


class Shops(models.Model):
    shop_name = models.CharField(max_length=15, verbose_name=_('shop_name'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))


    def __str__(self):
        return str(self.shop_name)

    def get_total_price(self):
        return sum(item.price for item in self.items.all())


class Items(models.Model):
    shop = models.ForeignKey('Shops', on_delete=models.CASCADE, blank=True, null=True, related_name='items',
                             verbose_name=_('shop'))
    item_name = models.CharField(max_length=300, verbose_name=_('item_name'))
    stocks = models.CharField(max_length=300, blank=True, verbose_name=_('stocks'))
    offers = models.CharField(max_length=300, blank=True, verbose_name=_('offers'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))
    quantity = models.PositiveIntegerField(default=0, verbose_name='кол-во')

    def __str__(self):
        return f'{self.item_name} - {self.price}'


class Purchase(models.Model):
    item = models.ForeignKey('Items', on_delete=models.CASCADE, verbose_name=_('item'))
    balance = models.ForeignKey('Balance', on_delete=models.CASCADE, verbose_name=_('balance'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('timestamp'))
    date = models.DateField(default=date.today, verbose_name=_('date'))

    def __str__(self):
        return f'{self.item.item_name} ({self.timestamp})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.balance.profile.total_spent += self.item.price
        self.balance.profile.save()
