from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DetailView, View
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView, LoginView
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
import logging


logger = logging.getLogger(__name__)


class ShopListView(ListView):
    model = Shops
    template_name = 'app_users/list_of_stores.html'

    def get(self, request, *args, **kwargs):
        logger.info('Запрошена страница со списком магазинов')
        return super().get(request, *args, **kwargs)


class ShopDetailView(DetailView):
    model = Shops
    template_name = 'app_users/market_detail.html'
    context_object_name = 'shop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items.all()
        context['items'] = items
        return context


class AnotherRegisterView(FormView):
    template_name = 'app_users/another_register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        Profile.objects.create(
            user=user,
            city=form.cleaned_data['city'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            phone=form.cleaned_data['phone'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
        )
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})


class AppLogin(LoginView):
    template_name = 'app_users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        logger.info(f"Пользователь {user.username} авторизовался.")
        return response


class LogoutNewsView(LogoutView):
    template_name = 'app_users/logout.html'


class AccountView(ListView):
    model = Profile
    template_name = 'app_users/account.html'
    context_object_name = 'acc'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        context['shop'] = Shops.objects.all()
        context['item'] = Items.objects.all()
        context['total_spent'] = self.request.user.profile.total_spent
        return context


class ReplenishBalanceView(LoginRequiredMixin, UpdateView):
    model = Balance
    form_class = ReplenishBalanceForm
    template_name = 'app_users/top_up_your_balance.html'
    success_url = reverse_lazy('account')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context

    def get_object(self):
        profile = self.request.user.profile
        balance, created = Balance.objects.get_or_create(profile=profile)
        return balance

    def form_valid(self, form):
        balance = form.cleaned_data['balance']
        balance_obj = self.get_object()
        balance_obj.balance += Decimal(balance)
        balance_obj.save()
        logger.info('Пользователь пополнил баланс')
        return super().form_valid(form)


class BuyItemView(View):
    @transaction.atomic
    def post(self, request, pk):
        item = get_object_or_404(Items, pk=pk)
        balance, created = Balance.objects.get_or_create(profile=request.user.profile)
        form = PurchaseForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if balance.balance >= item.price * quantity and item.quantity >= quantity:
                balance.balance -= item.price * quantity
                balance.save()
                logger.info(f'Баланс уменьшился на {item.price * quantity}')
                item.quantity -= quantity
                item.save()
                purchase = Purchase.objects.create(item=item, balance=balance)
                messages.success(request,
                                 f'Вы купили {quantity} штук товара "{item.item_name}" за {item.price * quantity} рублей.')
                logger.info(f'Пользователь купил товар {item.item_name} за {item.price * quantity} рублей')


                old_status = request.user.profile.status
                request.user.profile.total_spent += item.price * quantity
                request.user.profile.save()
                new_status = request.user.profile.status
                if old_status != new_status:
                    logger.info(f'Статус пользователя изменился.')

            else:
                messages.error(request,
                               'У вас недостаточно средств для покупки этого количества товара или товара нет в наличии.')
        else:
            messages.error(request, 'Неверное количество товара.')
        return redirect('detail', pk=item.shop.pk)


class HistoryView(ListView):
    model = Purchase
    template_name = 'app_users/history.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        balance = get_object_or_404(Balance, profile=self.request.user.profile)
        return Purchase.objects.filter(balance=balance)


class BestSellingProductsView(ListView):
    template_name = 'app_users/product_report.html'
    context_object_name = 'products'

    def get_queryset(self):
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        qs = Purchase.objects.filter(date__range=[start_date, end_date]) \
            .values('item__id', 'item__item_name') \
            .annotate(total_sold=Count('item')) \
            .order_by('-total_sold')
        return qs


