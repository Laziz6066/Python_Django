from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = '__all__'


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



    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)



class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ('activity',)


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ('news_comment', )



class ModerForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('is_published',)


class ModerUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active',)


