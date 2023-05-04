from django.db import models
from django.urls import reverse


class Housing(models.Model):
    name = models.CharField(max_length=100, verbose_name='название дома')
    description = models.TextField(verbose_name='содержимое')
    is_published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('house-item', args=[str(self.id)])

    def __str__(self):
        return self.name

class TypeOfRoom(models.Model):
    type_room = models.CharField(max_length=200, verbose_name='тип помещения')
    description = models.TextField(verbose_name='содержимое')
    house = models.ForeignKey(Housing, on_delete=models.CASCADE, verbose_name='дом')

    def __str__(self):
        return self.type_room

class NumberOfRooms(models.Model):
    numbers_room = models.IntegerField(verbose_name='кол-во комнат')
    house = models.ForeignKey(Housing, on_delete=models.CASCADE, verbose_name='дом')

    def __str__(self):
        return str(self.numbers_room)

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    text = models.TextField(verbose_name='текст')

    def __str__(self):
        return self.title