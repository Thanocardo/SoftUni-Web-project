from django.db import models

from learn_with_ease.user_profile.models import ProfileData
from learn_with_ease.web.validators import image_size_validator


# Create your models here.

class Folders(models.Model):

    folder_name = models.CharField(
        max_length=60,
    )

    archived = models.BooleanField(
        default=False,
    )

    profile_id = models.ForeignKey(
        to=ProfileData,
        related_name='folders',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )


class FlashCards(models.Model):

    question = models.TextField(
        null=True,
        blank=True,
    )

    question_pictures = models.ImageField(
        upload_to='flashcards/',
        null=True,
        blank=True,
        validators=[image_size_validator]
    )

    answer = models.TextField(
        null=True,
        blank=True,
    )

    answer_pictures = models.ImageField(
        upload_to='flashcards/',
        null=True,
        blank=True,
        validators=[image_size_validator]
    )

    shuffle_question_and_answer = models.BooleanField(
        default=False,
    )

    only_show_answer = models.BooleanField(
        default=True,
    )

    type_answer = models.BooleanField(
        default=False,
    )

    archived = models.BooleanField(
        default=False,
    )

    folder_id = models.ForeignKey(
        to=Folders,
        related_name='flashcards',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    profile_id = models.ForeignKey(
        to=ProfileData,
        related_name='flashcards',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

