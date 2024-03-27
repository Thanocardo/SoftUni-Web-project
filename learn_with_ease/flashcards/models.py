from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

from learn_with_ease.posts.models import Posts
from learn_with_ease.user_profile.models import ProfileData
from learn_with_ease.web.validators import image_size_validator


# Create your models here.

class Folders(models.Model):

    folder_name = models.CharField(
        max_length=60,
        validators=[MinLengthValidator(1)],
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

    post = models.ForeignKey(
        to=Posts,
        related_name="folders",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
        allow_unicode=True,
        default='none'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.folder_name:
                self.slug = slugify(unidecode(self.folder_name))
        super(Folders, self).save(*args, **kwargs)

    def copy(self):
        folder_copy = self.__class__.objects.create(
            folder_name=self.folder_name,
            folder_photo=self.folder_photo,
            slug=self.slug,
            archived=False,
            profile=None,
            post=None,
        )

        for flashcard in self.flashcards.all():
            flashcard_copy = flashcard.copy()
            flashcard_copy.folder = folder_copy
            flashcard_copy.save()

        return folder_copy

    def __str__(self):
        return self.folder_name


class FlashCards(models.Model):

    question = models.TextField(
        null=True,
        blank=True,
        default=None,
        validators=[MinLengthValidator(1)],
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
        validators=[MinLengthValidator(1)],
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
        allow_unicode=True,
        default='none'
        )

    folder = models.ForeignKey(
        to=Folders,
        related_name='flashcards',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    post = models.ForeignKey(
        to=Posts,
        related_name="flashcards",
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
        errors = []
        if not self.question and not self.question_picture:
            errors.append('Both question and question picture cannot be empty.')

        if not self.answer and not self.answer_picture:
            errors.append('Both answer and answer picture cannot be empty.')

        if errors:
            raise ValidationError(errors)

        if not self.slug:
            if self.question:
                unidecode_question = unidecode(self.question)
                self.slug = slugify(unidecode_question)
            else:
                unidecode_question = unidecode(self.question_picture.name)
                self.slug = slugify(unidecode(unidecode_question))
        super(FlashCards, self).save(*args, **kwargs)

    def copy(self):
        copy = self.__class__.objects.create(
            question=self.question,
            question_picture=self.question_picture,
            answer=self.answer,
            answer_picture=self.answer_picture,
            shuffle_question_and_answer=self.shuffle_question_and_answer,
            only_show_answer=self.only_show_answer,
            slug=self.slug,
            folder=None,
            archived=False,
            profile=None,
            post=None,
        )
        return copy

    def __str__(self):
        if self.question:
            return self.question
        else:
            return self.slug
