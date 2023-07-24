from apscheduler.schedulers.background import BackgroundScheduler
from game.models import Game, PlayedGame, DailyPlayedGame
from users.models import User
import pytz


def daily_reset_played_games():
    games = Game.objects.all()
    for game in games:
        n_top_player = game.num_of_users_get_gemyto
        daily_played_game = DailyPlayedGame.objects.filter(game=game).order_by('score')

        for daily_played in daily_played_game:
            user = User.objects.get(id=daily_played.user.id)
            earned_gemyto = daily_played.game_gemyto

            try:
                played = PlayedGame.objects.get(user=user, game=game)
                if daily_played.score > played.score:
                    played.score = daily_played.score
                if n_top_player > 0:
                    played.game_gemyto = played.game_gemyto + earned_gemyto
                    user.total_gemyto = user.total_gemyto + earned_gemyto
                    user.gemyto = user.gemyto + earned_gemyto
                    user.save()
                    n_top_player = n_top_player - 1
                played.save()
            except PlayedGame.DoesNotExist:
                if n_top_player > 0:
                    user.total_gemyto = user.total_gemyto + earned_gemyto
                    user.gemyto = user.gemyto + earned_gemyto
                    user.save()
                    n_top_player = n_top_player - 1
                else:
                    earned_gemyto = 0
                new_played = PlayedGame(game=daily_played.game, user=daily_played.user, game_gemyto=earned_gemyto,
                                        score=daily_played.score, created_at=daily_played.created_at)
                new_played.save()
            daily_played.delete()
        scores_game = game.scores

        if daily_played_game.exists():
            highest_score = daily_played_game.first()
            scores_game.max_value = highest_score.score
            scores_game.modify_scores()
            scores_game.save()
        game.modify_num_of_users_get_gemyto()
        game.save()


scheduler = BackgroundScheduler(timezone=pytz.utc)
scheduler.add_job(daily_reset_played_games, 'cron', hour=12)
scheduler.start()
