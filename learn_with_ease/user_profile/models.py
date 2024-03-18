from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinLengthValidator
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db import models

from learn_with_ease.user_profile.managers import AccountUserManager
from learn_with_ease.web.validators import image_size_validator, username_validator


# Create your models here.


class UserAccount(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        }
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    USERNAME_FIELD = "email"

    objects = AccountUserManager()


class ProfileData(models.Model):

    GENDER_CHOICES = (
        ("Man", "Man"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("Not specified", "Not specified"),
    )

    username = models.CharField(
        max_length=60,
        unique=True,
        validators=[username_validator, MinLengthValidator(3)]
    )

    profile_picture = models.ImageField(
        upload_to='profile_picture/',
        blank=True,
        null=True,
        validators=[image_size_validator],
    )

    age = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(120)],
        null=True,
        blank=True,
    )

    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=13,
        default="Not specified"
    )

    profile_description = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    slug = models.SlugField(
        unique=True,
        max_length=70,
        blank=True,
        )

    user = models.OneToOneField(
        UserAccount,
        on_delete=models.DO_NOTHING,
        primary_key=True,
        related_name="profile",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super(ProfileData, self).save(*args, **kwargs)
