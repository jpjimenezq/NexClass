# Generated by Django 5.0.2 on 2024-08-28 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialties', models.TextField()),
                ('biography', models.TextField()),
                ('average_rating', models.FloatField(default=0.0)),
                ('availability', models.CharField(choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Flexible', 'Flexible')], max_length=50)),
                ('mode', models.CharField(choices=[('Online', 'Online'), ('In-Person', 'In-Person'), ('Hybrid', 'Hybrid')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('user_type', models.CharField(choices=[('Student', 'Student'), ('Teacher', 'Teacher')], max_length=10)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('profile_picture', models.ImageField(blank=True, default='profile_photos/default_profile.png', null=True, upload_to='profile_photos/')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_complete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('className', models.CharField(max_length=100)),
                ('id_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorites', models.ManyToManyField(related_name='favorites', to='users.teacher')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('estudiante', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.student')),
                ('clase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.class')),
                ('profesor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.teacher')),
            ],
        ),
    ]
