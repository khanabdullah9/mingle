# Generated by Django 3.1 on 2022-02-01 08:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserProfile', '0008_auto_20220201_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_has_follower',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_has_follower',
            field=models.ManyToManyField(blank=True, null=True, related_name='some_random_string_1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_is_following',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_is_following',
            field=models.ManyToManyField(blank=True, null=True, related_name='some_random_string_2', to=settings.AUTH_USER_MODEL),
        ),
    ]