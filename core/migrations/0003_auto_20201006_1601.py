# Generated by Django 3.1.2 on 2020-10-06 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201006_1126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='name',
        ),
    ]
