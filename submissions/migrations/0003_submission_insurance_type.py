# Generated by Django 4.2.7 on 2024-04-21 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0002_submission_phone2_submission_pos_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='insurance_type',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]