# Generated by Django 5.1 on 2024-09-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0020_rename_cat_name_cat_name_remove_cat_instruction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='is_selected',
            field=models.BooleanField(default=True),
        ),
    ]
