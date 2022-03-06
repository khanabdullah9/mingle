# Generated by Django 4.0.2 on 2022-02-28 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserProfile', '0010_followrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrequest',
            name='requestee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]