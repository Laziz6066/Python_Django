from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




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


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class FileForms(forms.ModelForm):

    class Meta:
        model = FileModel
        fields = ('description', 'file', )


class MultiFileForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Загрузить')


class CsvUploadForm(forms.Form):
    file = forms.FileField()









