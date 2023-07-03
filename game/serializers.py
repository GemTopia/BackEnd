from rest_framework import serializers
from .models import Game, Report, GamePicture


class GameSerializer(serializers.ModelSerializer):
    is_liked_by_user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
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

    def get_like_count(self):
        return self.game_like.count()

    def get_game_pictures(self, obj):
        pictures = obj.game_picture.all()
        return GamePicture(instance=pictures, many=True).data

    def get_reports(self, obj):
        reports = obj.game_reports.all()
        return Report(instance=reports, many=True).data

    def get_num_of_report(self, obj):
        return obj.game_reports.count()


class ReportSerializer(serializers.Serializer):
    class Meta:
        model = Report
        fields = '__all__'
