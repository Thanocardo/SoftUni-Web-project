from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.template.defaultfilters import slugify
from unidecode import unidecode

from learn_with_ease.user_profile.models import ProfileData
from learn_with_ease.web.validators import image_size_validator


# Create your models here.

class Posts(models.Model):
    post_name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    likes = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        default=timezone.now,
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

    slug = models.SlugField(
        blank=True,
        allow_unicode=True,
        default='none'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            if self.post_name:
                self.slug = slugify(unidecode(self.post_name))
        super(Posts, self).save(*args, **kwargs)


class Comments(models.Model):
    comment = models.TextField(
        validators=[MinLengthValidator(1)],
    )

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    likes = models.PositiveIntegerField(
        default=0,
    )

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

