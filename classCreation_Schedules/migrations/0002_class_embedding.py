# Generated by Django 5.1.1 on 2024-10-21 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classCreation_Schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='embedding',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
