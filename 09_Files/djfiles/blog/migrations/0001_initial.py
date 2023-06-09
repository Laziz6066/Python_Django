# Generated by Django 4.1.4 on 2023-02-14 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='photo/')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Файлы блога',
                'verbose_name_plural': 'Файлы блога',
                'permissions': (('can_publish', 'Может публиковать'),),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('email', models.EmailField(max_length=35)),
                ('password', models.CharField(max_length=35)),
                ('city', models.CharField(blank=True, max_length=35)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogEntryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Содержание')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('published', models.DateTimeField(null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('download', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='download', to='blog.filemodel', verbose_name='Файл')),
            ],
            options={
                'verbose_name': 'Блог',
                'verbose_name_plural': 'Блог',
                'permissions': (('can_publish', 'Может публиковать'),),
            },
        ),
    ]
