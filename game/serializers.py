from rest_framework import serializers
from .models import Game, Report, GamePicture, Scores, DailyPlayedGame, Like


class GameSerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.SerializerMethodField()
    game_pictures = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = '__all__'

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.game_like.filter(user=request.user).exists()

        return False

    def get_game_pictures(self, obj):
        pictures = obj.game_picture.all()
        return GamePictureSerializer(instance=pictures, many=True).data


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = 'game', 'report_text'


class ScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = '__all__'


class DailyPlayedGameSerializer(serializers.ModelSerializer):
    gemyto = serializers.FloatField(default=0)
    game_name = serializers.CharField(source='game.name', allow_null=True, allow_blank=True)
    game_image = serializers.CharField(source='game.cover_image', allow_null=True, allow_blank=True)

    class Meta:
        model = DailyPlayedGame
        fields = ('game', 'user', 'score', 'gemyto', 'state', 'game_name', 'game_image')


class GamePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePicture
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'
