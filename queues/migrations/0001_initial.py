# Generated by Django 4.2.6 on 2023-10-30 14:44

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
            name='Queue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('descreption', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('shift_start', models.TimeField(blank=True, null=True)),
                ('shift_end', models.TimeField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('queue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='queues.queue')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='queue',
            name='user',
            field=models.ManyToManyField(through='queues.UserQueue', to=settings.AUTH_USER_MODEL),
        ),
    ]
