from django.core.exceptions import ValidationError
import re

def image_size_validator(image):
    SIZE_10_MB = 10 * 1024 * 1024

    if image.size >SIZE_10_MB:
        raise ValidationError("Max size of file is 10 MB.")


def username_validator(username):
    regex = r"\W"

    if re.search(regex, username):
        return ValidationError("Username must contain only letters, numbers and underscores.")