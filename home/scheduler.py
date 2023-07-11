from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from game.models import DailyPlayedGame, PlayedGame, Game, Scores
from users.models import User






def daily_task():
    games = Game.objects.all()
    for game in games:
        n_top_player = game.num_of_users_get_gemyto
        daily_played_game = DailyPlayedGame.objects.filter(game=game).order_by('score')

        for daily_played in daily_played_game:
            user = User.objects.get(id=daily_played.user.id)
            earned_gemyto = daily_played.gemyto
            played = PlayedGame.objects.get(user=user, game=game)
            if played.exists():
                if daily_played.score > played.score:
                    played.score = daily_played.score
                if n_top_player > 0:
                    played.gemyto = played.gemyto + earned_gemyto
                    user.total_gemyto = user.total_gemyto + earned_gemyto
                    user.save()
                    n_top_player = n_top_player - 1
                played.save()
            else:
                if n_top_player > 0:

                    user.total_gemyto = user.total_gemyto + earned_gemyto
                    user.save()
                    n_top_player = n_top_player - 1
                else:
                    earned_gemyto = 0
            new_played = PlayedGame(game=daily_played.game, user=daily_played.user, gemyto=earned_gemyto,
                                    score=daily_played.score, created_at=daily_played.created_at)
            new_played.save()
        scores_game = Scores.objects.get(game=game)
        highest_score = daily_played_game.first()
        scores_game.max_value = highest_score.score
        scores_game.modify_scores()
    Game.modify_num_of_users_get_gemyto()
#
#
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), "default")
#     scheduler.add_job(
#         # daily_task,
#         trigger="cron",
#         hour=12,
#         timezone="Etc/Greenwich",
#     )
#     scheduler.start()
