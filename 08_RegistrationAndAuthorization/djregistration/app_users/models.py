from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from taggit.managers import TaggableManager


class Tag(models.Model):
    tag = models.CharField(max_length=50, verbose_name='Тег')


class News(models.Model):
    title = models.CharField(max_length=30, verbose_name='Заголовок')
    description = models.TextField(default='', verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    date_edit = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    activity = models.IntegerField(default=0, verbose_name='Кол-во комментариев')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    tags = models.ManyToManyField(Tag, related_name='Тег')

    def get_absolute_url(self):
        return reverse('news')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        permissions = (
            ('can_publish', 'Может публиковать'),
        )

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=30, verbose_name='Пользователь')
    description = models.TextField(default='', verbose_name='Текст комментария')
    news_comment = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.user_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.EmailField(max_length=35)
    password = models.CharField(max_length=35)
    city = models.CharField(max_length=35, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('blog')


