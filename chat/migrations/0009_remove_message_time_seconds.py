# Generated by Django 4.0.2 on 2022-03-25 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_alter_message_message_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='time_seconds',
        ),
    ]