# Generated by Django 4.0.2 on 2022-03-25 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_remove_message_time_seconds'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_time',
            field=models.DateTimeField(),
        ),
    ]
