# Generated by Django 4.2.7 on 2024-04-25 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0003_submission_insurance_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Closers',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LeaderStatus',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='submission',
            name='closer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='submissions.closers'),
        ),
        migrations.AddField(
            model_name='submission',
            name='leader_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='submissions.leaderstatus'),
        ),
    ]
