from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


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


class BlogEntryModel(models.Model):
    description = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)



    def get_absolute_url(self):
        return reverse('blog')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'
        permissions = (
            ('can_publish', 'Может публиковать'),
        )

    def __str__(self):
        return str(self.created_at)

class FileModel(models.Model):
    file = models.FileField(upload_to='photo/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    download = models.ForeignKey('BlogEntryModel', on_delete=models.CASCADE,
                                 related_name='download', verbose_name='Файл', null=True)


    def get_absolute_url(self):
        return reverse('blog')

    class Meta:
        verbose_name = 'Файлы блога'
        verbose_name_plural = 'Файлы блога'
        permissions = (
            ('can_publish', 'Может публиковать'),
        )

    def __str__(self):
        return str(self.description)


