from rest_framework import serializers
from landing.models import EmailForNews, GemytoInfo
from datetime import datetime


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailForNews
        fields = ('email',)

    def create(self, validated_data):
        return EmailForNews.objects.create(**validated_data, )


class GemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GemytoInfo
        fields = ('token_value',)

    def create(self, validated_data):
        validated_data['created_at'] = now = datetime.now()
        return GemytoInfo.objects.create(**validated_data)
