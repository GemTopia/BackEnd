from django.db import models
from users.models import User
from game_master.models import GameMaster
from django.core.validators import ValidationError, FileExtensionValidator
from GemTopia import settings


def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))

def game_picture_directory_path(instance, filename):
    return 'game/{0}/picture/{1}'.format(str(instance.game.name), filename)

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

    num_of_users_get_gemyto = models.PositiveIntegerField(default=20)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def modify_num_of_users_get_gemyto(self):
        N = 20
        game_rank = Game.objects.filter(num_of_like__gt=self.num_of_like).aggregate(rank=Count('num_of_like'))[
                        'rank'] + 1
        num_of_total_games = Game.objects.count()
        totalN = num_of_total_games * N;
        self.num_of_users_get_gemyto = math.ceil(
            (num_of_total_games - game_rank) * totalN / (num_of_total_games * (num_of_total_games + 1)))

    def str(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        db_table = 'game'


class PlayedGame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_players')
    game_gemyto = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)

    def str(self):
        return f'{self.user} played {self.game}'

    class Meta:
        ordering = ['score']
        verbose_name = 'played game'
        verbose_name_plural = 'played games'
        db_table = 'played_game'

class DailyPlayedGame(models.Model):
    STATE_CHOICES = (
        (1, 'State 1'),
        (2, 'State 2'),
        (3, 'State 3'),
        (4, 'State 4'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_daily_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_daily_players')
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    deleted_at = models.DateField(null=True)
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=0)

    def str(self):
        return f'{self.user} played {self.game} daily'

    class Meta:
        ordering = ['score']
        verbose_name = ' daily played game'
        verbose_name_plural = 'daily played games'
        db_table = 'daily_played_game'



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

