# Generated by Django 4.2.2 on 2023-07-20 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reports', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playedgame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_players', to='game.game'),
        ),
        migrations.AddField(
            model_name='playedgame',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_games', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='like',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_like', to='game.game'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gamepicture',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_picture', to='game.game'),
        ),
        migrations.AddField(
            model_name='game',
            name='scores',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='score_game', to='game.scores'),
        ),
        migrations.AddField(
            model_name='dailyplayedgame',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_daily_players', to='game.game'),
        ),
        migrations.AddField(
            model_name='dailyplayedgame',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_daily_games', to=settings.AUTH_USER_MODEL),
        ),
    ]
