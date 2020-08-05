# Generated by Django 3.0.8 on 2020-08-04 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=20)),
                ('goal', models.IntegerField(blank=True, default=0)),
                ('taste', models.CharField(blank=True, max_length=20)),
                ('already', models.IntegerField(blank=True, default=0)),
                ('follows', models.ManyToManyField(blank=True, related_name='followed', through='accounts.Follow', to='accounts.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='follow',
            name='follow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed_by', to='accounts.Profile'),
        ),
        migrations.AddField(
            model_name='follow',
            name='followed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow', to='accounts.Profile'),
        ),
    ]
