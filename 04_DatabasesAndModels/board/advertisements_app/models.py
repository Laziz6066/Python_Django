from django.db import models
from django.urls import reverse


class Ads(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.CharField(max_length=100, verbose_name='Цена')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    views_count = models.IntegerField(verbose_name='кол-во просмотров', default=0)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category', verbose_name='Категория')

    def __str__(self):
        return self.title

    def incrementViewCount(self):
        self.views_count += 1
        self.save()

    class Meta:
        db_table = 'advertisement'
        ordering = ['title']
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'


class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    emaill = models.CharField(max_length=254, null=True, verbose_name='Email')
    number = models.CharField(max_length=15, null=True, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Авторы'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')


    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

