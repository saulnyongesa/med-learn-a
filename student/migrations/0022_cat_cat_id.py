# Generated by Django 5.1 on 2024-09-02 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_response_is_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='cat_id',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]