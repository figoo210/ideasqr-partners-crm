# Generated by Django 4.2.7 on 2024-04-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='phone2',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='pos_type',
            field=models.CharField(default=1, max_length=4),
            preserve_default=False,
        ),
    ]