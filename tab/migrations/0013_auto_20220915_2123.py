# Generated by Django 3.2.15 on 2022-09-15 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0012_auto_20220915_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='messages',
            field=models.TextField(default='', max_length=120),
        ),
        migrations.AlterField(
            model_name='taught',
            name='taught',
            field=models.TextField(default='', max_length=80),
        ),
    ]
