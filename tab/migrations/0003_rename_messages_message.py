# Generated by Django 3.2.15 on 2022-09-13 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('tab', '0002_messages_user_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
    ]
