from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    email = forms.EmailField(max_length=70)
    date_of_birth = forms.DateField(required=False, help_text='Дата рождения')
    city = forms.CharField(max_length=35, required=True, help_text='Город проживания')
    phone = forms.CharField(max_length=15, required=True, help_text='Номер телефона')



class ReplenishBalanceForm(forms.ModelForm):
    class Meta:
        model = Balance
        fields = ['balance']


class PurchaseForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
