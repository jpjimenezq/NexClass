# Generated by Django 5.1 on 2024-08-21 05:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('user_type', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], max_length=10)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pictures/default.jpg', null=True, upload_to='profile_pictures/')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialties', models.TextField()),
                ('biography', models.TextField()),
                ('average_rating', models.FloatField(default=0.0)),
                ('availability', models.CharField(choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Flexible', 'Flexible')], max_length=50)),
                ('hourly_rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mode', models.CharField(choices=[('Online', 'Online'), ('In-Person', 'In-Person'), ('Hybrid', 'Hybrid')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorites', models.ManyToManyField(related_name='favorites', to='users.teacher')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
    ]
