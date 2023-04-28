from django.db import models


class Book(models.Model):
    """Модель для книги"""
    title = models.CharField(max_length=255, verbose_name='Название книги')
    isbn = models.IntegerField(verbose_name='Мскн')
    year_of_release = models.DateField(verbose_name='Год выпуска')
    number_of_pages = models.IntegerField(verbose_name='Кол-во страниц')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='author', verbose_name='Автор')

    def __str__(self):
        return self.title

class Author(models.Model):
    """Модель авторов."""
    name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    date_of_birth = models.DateField(verbose_name='Дата рождения')

    def __str__(self):
        return self.name