from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import ValidationError, FileExtensionValidator
from django.template.defaultfilters import filesizeformat


def user_avatar_directory_path(instance, filename):
    return 'user/{0}/avatar/{1}'.format(str(instance.username), filename)


def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))


class User(AbstractUser):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']
    email = models.EmailField(unique=True)
    inviter = models.ForeignKey('self', on_delete=models.CASCADE, related_name='invited', blank=True, null=True)
    referrer_code = models.CharField(max_length=90, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True)
    total_gemyto = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','password']

    class Meta:
        ordering = ['created_at']
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
