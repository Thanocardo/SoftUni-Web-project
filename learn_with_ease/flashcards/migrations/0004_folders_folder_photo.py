# Generated by Django 4.2.4 on 2024-03-17 18:09

from django.db import migrations, models
import learn_with_ease.web.validators


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0003_alter_flashcards_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='folders',
            name='folder_photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='folders/', validators=[learn_with_ease.web.validators.image_size_validator]),
        ),
    ]