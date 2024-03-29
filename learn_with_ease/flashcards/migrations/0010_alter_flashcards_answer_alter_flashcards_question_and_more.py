# Generated by Django 4.2.4 on 2024-03-26 15:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0009_alter_flashcards_slug_alter_folders_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcards',
            name='answer',
            field=models.TextField(blank=True, default=None, null=True, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
        migrations.AlterField(
            model_name='flashcards',
            name='question',
            field=models.TextField(blank=True, default=None, null=True, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
        migrations.AlterField(
            model_name='folders',
            name='folder_name',
            field=models.CharField(max_length=60, validators=[django.core.validators.MinLengthValidator(1)]),
        ),
    ]
