# Generated by Django 3.2.15 on 2022-09-14 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0006_remove_message_taught'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taught',
            name='taught',
            field=models.TextField(default='[]', max_length=80),
        ),
    ]