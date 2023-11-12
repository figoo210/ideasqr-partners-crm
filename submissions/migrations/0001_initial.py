# Generated by Django 4.2.6 on 2023-10-30 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('queues', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('medical_id', models.CharField(max_length=11)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('middle_initial', models.CharField(blank=True, max_length=20, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('birth_date', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=10)),
                ('comment', models.CharField(max_length=255)),
                ('products', models.ManyToManyField(blank=True, through='products.SubmissionProducts', to='products.product')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='submissions.status')),
                ('user_queue', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='queues.userqueue')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
