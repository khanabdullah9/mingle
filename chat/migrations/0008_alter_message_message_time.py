# Generated by Django 4.0.2 on 2022-03-24 16:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_alter_message_message_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
