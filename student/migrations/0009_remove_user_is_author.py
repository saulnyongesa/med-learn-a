# Generated by Django 5.1 on 2024-08-30 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_user_is_author_user_is_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_author',
        ),
    ]
