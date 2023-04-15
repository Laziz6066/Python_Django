# Generated by Django 4.1.4 on 2023-01-29 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_rename_username_profile_user_news_is_published_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50, verbose_name='Тег')),
            ],
        ),
        migrations.RemoveField(
            model_name='news',
            name='tags',
        ),
        migrations.AddField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(related_name='Тег', to='blog.tag'),
        ),
    ]
