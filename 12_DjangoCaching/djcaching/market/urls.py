from django.urls import path
from .views import *


urlpatterns = [
    path('', ShopListView.as_view(), name='home'),
    path('login', AppLogin.as_view(), name='login'),
    path('logout', LogoutNewsView.as_view(), name='logout'),
    path('register', AnotherRegisterView.as_view(), name='another_register'),
    path('account', AccountView.as_view(), name='account'),
    path('account/<int:profile_id>/top_up_your_balance/', ReplenishBalanceView.as_view(), name='top_up_your_balance'),
    path('<int:pk>/detail', ShopDetailView.as_view(), name='detail'),
    path('buy/<int:pk>/', BuyItemView.as_view(), name='buy_item'),
    path('history', HistoryView.as_view(), name='history'),
]