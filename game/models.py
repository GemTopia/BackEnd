from django.db import models
from GemTopia import settings
from users.models import User
from game_master.models import GameMaster
from django.template.defaultfilters import filesizeformat
from django.core.validators import ValidationError, FileExtensionValidator
import math


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
    link = models.URLField(null=True)
    num_of_like = models.PositiveIntegerField(default=0)
    num_of_report = models.PositiveIntegerField(default=0)
    game_type = models.CharField(max_length=90)
    game_master = models.ForeignKey(GameMaster, on_delete=models.SET_NULL, related_name='game_master_games', null=True)
    is_active = models.BooleanField(default=True)
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


class Scores(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_scores')
    max_value = models.PositiveIntegerField(null=False)
    first_level_score = models.PositiveIntegerField(null=True)
    second_level_score = models.PositiveIntegerField(null=True)
    third_level_score = models.PositiveIntegerField(null=True)
    fourth_level_score = models.PositiveIntegerField(null=True)
    distance = models.PositiveIntegerField(default=0)

    def modeify_scors(self):
        self.distance = math.log(self.max_value, 2)
        self.first_level_score = 2 ** (self.distance / 4)
        self.second_level_score = 2 ** ((2 * self.distance) / 4)
        self.third_level_score = 2 ** ((3 * self.distance) / 4)
        self.fourth_level_score = self.max_value

    def __str__(self):
        return f'{self.game.name}-{self.max_value}'

    class Meta:
        db_table = 'scores'


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
    gemyto = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def __str__(self):
        return f'{self.user} played {self.game}'

    class Meta:
        ordering = ['score']
        verbose_name = 'played game'
        verbose_name_plural = 'played games'
        db_table = 'played_game'


class DailyPlayedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_daily_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_daily_players')
    score = models.PositiveIntegerField(default=0)
    gemyto = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)
    num_of_users_get_gemyto = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f'{self.user} played {self.game} daily'

    class Meta:
        ordering = ['score']
        verbose_name = ' daily  played game'
        verbose_name_plural = 'daily played games'
        db_table = 'daily_played_game'
