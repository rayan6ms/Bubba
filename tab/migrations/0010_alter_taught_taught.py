# Generated by Django 3.2.15 on 2022-09-14 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0009_alter_taught_taught'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taught',
            name='taught',
            field=models.TextField(default=None, max_length=80),
        ),
    ]
