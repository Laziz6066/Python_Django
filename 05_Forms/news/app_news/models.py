from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import  get_user_model


def get_sentinel_user (*args):
    return get_user_model().objects.get_or_create(username=args[0])[0]


class News(models.Model):
    title = models.CharField(max_length=1000, verbose_name='название статьи')
    description = models.CharField(max_length=10000, verbose_name='содержание статьи')
    date_create = models.DateField(auto_now_add=True, verbose_name='дата публикации')
    date_edit = models.DateField(auto_now=True, verbose_name='дата редактирования')
    activity = models.IntegerField(default=0, verbose_name='количество комментариев')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class Comment(models.Model):
    user_name = models.CharField(max_length=100, verbose_name='имя пользователя')
    description = models.CharField(max_length=10000, verbose_name='текст комментария')
    news_comment = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments',
                                     verbose_name='Новость')
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), blank=True, null=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
