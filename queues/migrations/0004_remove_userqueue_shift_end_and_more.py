# Generated by Django 4.2.6 on 2023-11-06 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0003_alter_queue_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userqueue',
            name='shift_end',
        ),
        migrations.RemoveField(
            model_name='userqueue',
            name='shift_start',
        ),
    ]
