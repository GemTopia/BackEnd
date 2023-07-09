from rest_framework import serializers
from users.models import User, SocialMedia
from game.models import DailyPlayedGame


class DailyPlayedGameSerializer(serializers.ModelSerializer):
    gemyto = serializers.IntegerField(default=0)

    class Meta:
        model = DailyPlayedGame
        fields = ('game', 'user', 'score','gemyto')