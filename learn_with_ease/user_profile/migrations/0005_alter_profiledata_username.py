# Generated by Django 4.2.4 on 2024-03-26 15:57

from django.db import migrations, models
import learn_with_ease.web.validators


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_alter_profiledata_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiledata',
            name='username',
            field=models.CharField(error_messages={'unique': 'This username already exists.'}, max_length=60, unique=True, validators=[learn_with_ease.web.validators.username_validator]),
        ),
    ]
