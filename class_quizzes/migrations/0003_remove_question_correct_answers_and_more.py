# Generated by Django 5.1 on 2024-10-14 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('class_quizzes', '0002_remove_question_number_correct_answers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_answers',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_type',
        ),
        migrations.RemoveField(
            model_name='question',
            name='total_answers',
        ),
    ]
