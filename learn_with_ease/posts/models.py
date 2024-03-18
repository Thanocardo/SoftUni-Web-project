from django.db import models
from django.utils import timezone

from learn_with_ease.flashcards.models import FlashCards, Folders
from learn_with_ease.user_profile.models import ProfileData
from learn_with_ease.web.validators import image_size_validator


# Create your models here.

class Posts(models.Model):
    post_name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    like = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    cards = models.ManyToManyField(
        to=FlashCards,
        related_name="posts_data"
    )

    folders = models.ManyToManyField(
        to=Folders,
        related_name="posts_data"
    )

    post_photo = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        validators=[image_size_validator]
    )

    profile = models.ForeignKey(
        to=ProfileData,
        related_name="posts",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )


class Comments(models.Model):
    comment = models.TextField()

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    likes = models.PositiveIntegerField()

    post = models.ForeignKey(
        to=Posts,
        related_name="comments",
        on_delete=models.DO_NOTHING,
    )

    profile = models.ForeignKey(
        to=ProfileData,
        related_name="comments",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )

