# Generated by Django 4.1.4 on 2023-01-02 10:53

import app_news.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_news', '0002_comment_user_alter_comment_news_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(app_news.models.get_sentinel_user), to=settings.AUTH_USER_MODEL),
        ),
    ]
