from django.db import models
from django.utils.text import slugify

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

    folder_photo = models.ImageField(
        upload_to='folders/',
        null=True,
        blank=True,
        validators=[image_size_validator],
        default=None,
    )

    profile = models.ForeignKey(
        to=ProfileData,
        related_name='folders',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.folder_name:
                self.slug = slugify(self.folder_name)
        super(Folders, self).save(*args, **kwargs)

    def __str__(self):
        return self.folder_name


class FlashCards(models.Model):

    question = models.TextField(
        null=True,
        blank=True,
        default=None,
    )

    question_picture = models.ImageField(
        upload_to='flashcards/',
        null=True,
        blank=True,
        validators=[image_size_validator],
        default=None,
    )

    answer = models.TextField(
        null=True,
        blank=True,
        default=None,
    )

    answer_picture = models.ImageField(
        upload_to='flashcards/',
        null=True,
        blank=True,
        validators=[image_size_validator],
        default=None,
    )

    shuffle_question_and_answer = models.BooleanField(
        default=False,
    )

    only_show_answer = models.BooleanField(
        default=True,
    )

    archived = models.BooleanField(
        default=False,
    )

    slug = models.SlugField(
        blank=True,
        )

    folder = models.ForeignKey(
        to=Folders,
        related_name='flashcards',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    profile = models.ForeignKey(
        to=ProfileData,
        related_name='flashcards',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.question:
                self.slug = slugify(self.question)
            else:
                self.slug = slugify(self.question_picture.name)
        super(FlashCards, self).save(*args, **kwargs)

