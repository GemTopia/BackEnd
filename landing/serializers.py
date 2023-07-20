from rest_framework import serializers
from landing.models import GemytoInfo
from django.utils import timezone


class GemInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GemytoInfo
        fields = ('value',)

    def create(self, validated_data):
        pass