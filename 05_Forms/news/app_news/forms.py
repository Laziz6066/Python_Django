from django import forms
from .models import Comment, News


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ('activity', )


class NewsCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user_name', 'description']
        exclude = ('news_comment', )


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)