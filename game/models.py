from django.core.validators import ValidationError, FileExtensionValidator
from django.db.models.signals import post_save, post_delete
from django.template.defaultfilters import filesizeformat
from django.dispatch import receiver
from django.db import models
from GemTopia import settings
from users.models import User
import math


def game_picture_directory_path(instance, filename):
    return 'game/{0}/picture/{1}'.format(str(instance.name), filename)


def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('Max image size should be '.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))


class Scores(models.Model):
    max_value = models.PositiveIntegerField(default=0)
    first_level_score = models.PositiveIntegerField(default=0, null=True, blank=True)
    second_level_score = models.PositiveIntegerField(default=0, null=True, blank=True)
    third_level_score = models.PositiveIntegerField(default=0, null=True, blank=True)
    fourth_level_score = models.PositiveIntegerField(default=0, null=True, blank=True)
    distance = models.PositiveIntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.modify_scores()
        super().save(*args, **kwargs)

    def modify_scores(self):
        if self.max_value <= 0:
            self.distance = 0
        else:
            self.distance = math.log(self.max_value, 2)
        self.first_level_score = 2 ** (self.distance / 4)
        self.second_level_score = 2 ** ((2 * self.distance) / 4)
        self.third_level_score = 2 ** ((3 * self.distance) / 4)
        self.fourth_level_score = self.max_value

    def save(self, *args, **kwargs):
        self.modify_scores()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.max_value}'

    class Meta:
        db_table = 'scores'


class Game(models.Model):
    GAME_TYPE_CHOICES = (
        ('action', 'action'),
        ('shooting', 'shooting'),
        ('quiz', 'quiz'),
        ('sport', 'sport'),
        ('puzzle', 'puzzle'),
    )
    VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']
    bio = models.TextField()
    name = models.CharField(max_length=200)
    link = models.URLField(null=True)
    rank = models.PositiveIntegerField(default=0, editable=False)
    num_of_like = models.PositiveIntegerField(default=0, editable=False)
    num_of_report = models.PositiveIntegerField(default=0)
    game_type = models.CharField(
        max_length=20,
        choices=GAME_TYPE_CHOICES
    )

    is_active = models.BooleanField(default=True)
    cover_image = models.ImageField(upload_to=game_picture_directory_path,
                                    validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                                    blank=True, null=True)
    logo_image = models.ImageField(upload_to=game_picture_directory_path,
                                   validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                                   blank=True, null=True)
    num_of_users_get_gemyto = models.PositiveIntegerField(default=20, null=True, blank=True)
    scores = models.ForeignKey(Scores, on_delete=models.CASCADE, related_name='score_game')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            score = Scores.objects.create()
            self.scores = score
        super().save(*args, **kwargs)

    def modify_num_of_users_get_gemyto(self):
        N = 20
        game_rank = self.rank
        num_of_total_games = Game.objects.count()
        totalN = num_of_total_games * N
        a = totalN / (num_of_total_games * (num_of_total_games + 1) / 2)
        self.num_of_users_get_gemyto = a * (num_of_total_games - game_rank + 1)

    def calculate_and_set_rank(self):
        games_with_more_likes = Game.objects.filter(num_of_like__gt=self.num_of_like)
        games_with_equal_likes = Game.objects.filter(num_of_like=self.num_of_like)

        games_with_more_likes_count = games_with_more_likes.count()
        games_with_equal_likes_earlier = games_with_equal_likes.filter(created_at__lt=self.created_at)
        games_with_equal_likes_earlier_count = games_with_equal_likes_earlier.count()

        game_rank = games_with_more_likes_count + games_with_equal_likes_earlier_count + 1
        self.rank = game_rank

    def update_all_game_ranks(self):
        games = Game.objects.all()
        for game in games:
            game.calculate_and_set_rank()
            game.save()

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.report_text

    class Meta:
        ordering = ['created_at']
        db_table = 'report'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_like')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True)

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
    game_gemyto = models.FloatField(default=0)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    state = models.PositiveIntegerField(choices=STATE_CHOICES, default=0)
    game_gemyto = models.FloatField(default=0)
    is_new_record = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f'{self.user} played {self.game} daily'

    class Meta:
        ordering = ['score']
        verbose_name = ' daily  played game'
        verbose_name_plural = 'daily played games'
        db_table = 'daily_played_game'


@receiver(post_save, sender=Report)
def update_num_of_report_on_report_save(sender, instance, **kwargs):
    game = instance.game
    game.num_of_report = game.game_reports.count()
    game.save()


@receiver(post_save, sender=Like)
def update_num_of_like_on_like_save(sender, instance, **kwargs):
    game = instance.game
    game.num_of_like = game.game_like.count()
    game.save()
    Game().update_all_game_ranks()


@receiver(post_delete, sender=Like)
def update_num_of_like_on_like_delete(sender, instance, **kwargs):
    game = instance.game
    game.num_of_like = game.game_like.count()
    game.save()
    Game().update_all_game_ranks()
