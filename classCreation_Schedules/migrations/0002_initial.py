# Generated by Django 5.1 on 2024-11-09 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classCreation_Schedules', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teacher'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='class_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='classCreation_Schedules.class'),
        ),
    ]
