# Generated by Django 3.2.15 on 2022-09-14 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0005_taught'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='taught',
        ),
    ]
