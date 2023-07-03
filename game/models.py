from django.db import models
from GemTopia import settings
from users.models import User
from game_master.models import GameMaster
from django.template.defaultfilters import filesizeformat
from django.core.validators import ValidationError, FileExtensionValidator


def game_picture_directory_path(instance, filename):
    return 'game/{0}/picture/{1}'.format(str(instance.game.name), filename)


def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))


class Game(models.Model):
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']
    bio = models.TextField()
    name = models.CharField(max_length=200)
    num_of_report = models.IntegerField(default=0)
    game_type = models.CharField(max_length=90)
    game_master = models.ForeignKey(GameMaster, on_delete=models.SET_NULL, related_name='game_master_games', null=True)
    is_active = models.BooleanField()
    cover_image = models.ImageField(upload_to=game_picture_directory_path,
                                    validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                                    blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        db_table = 'game'


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reports')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_reports')
    report_text = models.TextField()
    validate = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return self.report_text

    class Meta:
        ordering = ['created_at']
        db_table = 'report'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_like')
    created_at = models.DateField(auto_now_add=True)
    deleted_at = models.DateField()

    def __str__(self):
        return f'{self.user} liked {self.game}'

    class Meta:
        ordering = ['created_at']
        db_table = 'like'


class GamePicture(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_picture')
    picture = models.ImageField(upload_to=game_picture_directory_path, blank=True, null=True)

    class Meta:
        db_table = 'game_picture'


class PlayedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_players')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return f'{self.user} played {self.game}'

    class Meta:
        ordering = ['updated_at']
        verbose_name = 'played game'
        verbose_name_plural = 'played games'
        db_table = 'playes_game'
