# Generated by Django 3.0.8 on 2020-08-03 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_merge_20200731_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='already_read',
            new_name='already',
        ),
    ]
