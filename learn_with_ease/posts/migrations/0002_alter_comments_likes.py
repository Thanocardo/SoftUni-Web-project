# Generated by Django 4.2.4 on 2024-03-24 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]