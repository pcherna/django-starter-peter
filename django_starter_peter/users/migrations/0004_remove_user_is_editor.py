# Generated by Django 2.2.9 on 2020-01-21 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200121_0428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_editor',
        ),
    ]
