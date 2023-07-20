from rest_framework import serializers

from .models import Game, Report, GamePicture, Scores, DailyPlayedGame, Like


class GameSerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.SerializerMethodField()
    num_of_like = serializers.SerializerMethodField()
    game_pictures = serializers.SerializerMethodField()
    reports = serializers.SerializerMethodField()
    num_of_report = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = '__all__'

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return obj.game_like.filter(user=request.user).exists()

        return False

    def get_num_of_like(self, obj):
        return obj.game_like.count()

    def get_game_pictures(self, obj):
        pictures = obj.game_picture.all()
        return GamePictureSerializer(instance=pictures, many=True).data

    def get_reports(self, obj):
        reports = obj.game_reports.all()
        return ReportSerializer(instance=reports, many=True).data

    def get_num_of_report(self, obj):
        return obj.game_reports.count()


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scores
        fields = '__all__'


class DailyPlayedGameSerializer(serializers.ModelSerializer):
    gemyto = serializers.IntegerField(default=0)

    class Meta:
        model = DailyPlayedGame
        fields = ('game', 'user', 'score', 'gemyto')


class GamePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePicture
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.BooleanField(read_only=True)

    class Meta:
        model = Like
        fields = '__all__'