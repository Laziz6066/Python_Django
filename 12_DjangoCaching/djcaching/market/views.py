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


class ShopListView(ListView):
    model = Shops
    template_name = 'market/list_of_stores.html'


class ShopDetailView(DetailView):
    model = Shops
    template_name = 'market/market_detail.html'
    context_object_name = 'shop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cache_key = f'shop_items_{self.object.pk}'
        items = cache.get(cache_key)

        if items is None:
            items = self.object.items.all()
            cache.set(cache_key, items, 30 * 60)

        context['items'] = items
        return context

class AnotherRegisterView(FormView):
    template_name = 'market/another_register.html'
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
    template_name = 'market/login.html'


class LogoutNewsView(LogoutView):
    template_name = 'market/logout.html'


class AccountView(ListView):
    model = Profile
    template_name = 'market/account.html'
    context_object_name = 'acc'

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        context['shop'] = Shops.objects.all()
        context['item'] = Items.objects.all()
        return context


class ReplenishBalanceView(UpdateView):
    model = Balance
    form_class = ReplenishBalanceForm
    template_name = 'market/top_up_your_balance.html'
    success_url = reverse_lazy('account')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile
        return context

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id)
        balance, created = Balance.objects.get_or_create(profile=profile)
        return balance

    def form_valid(self, form):
        balance = form.cleaned_data['balance']
        balance_obj = self.get_object()
        balance_obj.balance += Decimal(balance)
        balance_obj.save()
        return super().form_valid(form)


class BuyItemView(View):
    def post(self, request, pk):
        item = get_object_or_404(Items, pk=pk)
        balance, created = Balance.objects.get_or_create(profile=request.user.profile)
        if balance.balance >= item.price:
            balance.balance -= item.price
            balance.save()
            purchase = Purchase.objects.create(item=item, balance=balance)
            messages.success(request, f'Вы купили товар "{item.item_name}" за {item.price} рублей.')
        else:
            messages.error(request, 'У вас недостаточно средств для покупки этого товара.')
        return redirect('detail', pk=item.shop.pk)


class HistoryView(ListView):
    model = Purchase
    template_name = 'market/history.html'
    context_object_name = 'purchases'

    def get_queryset(self):
        balance = get_object_or_404(Balance, profile=self.request.user.profile)
        return Purchase.objects.filter(balance=balance)