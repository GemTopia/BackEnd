from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from GemTopia import settings
from django.core.validators import ValidationError, FileExtensionValidator
from django.template.defaultfilters import filesizeformat
from users.managers import UserManager


def user_avatar_directory_path(instance, filename):
    return 'users/{0}/avatar/{1}'.format(str(instance.user_name), filename)


def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))


class User(AbstractBaseUser, PermissionsMixin):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    inviter = models.ForeignKey('self', on_delete=models.CASCADE, related_name='invited', blank=True, null=True)
    referrer_code = models.CharField(max_length=90, blank=True, null=True)
    avatar = models.ImageField(upload_to=user_avatar_directory_path,
                               validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                               blank=True, null=True)
    total_gemyto = models.IntegerField(default=0)
    gemyto=models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'password']

    class Meta:
        ordering = ['created_at']
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'user'

    def __str__(self):
        return str(self.id)

    @property
    def is_staff(self):
        return self.is_admin
