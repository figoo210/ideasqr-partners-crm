# Generated by Django 4.2.6 on 2023-11-02 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queue',
            old_name='descreption',
            new_name='description',
        ),
    ]
