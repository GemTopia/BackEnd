from users.models import User, SocialMedia
from game.serializers import GameSerializer
from django.contrib.auth import password_validation
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'email', 'password', 'gemyto')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data, referrer_code=None):
        if referrer_code:
            inviter_id = User.objects.filter(referrer_code=referrer_code).values_list('id', flat=True).first()
            if inviter_id is not None:
                inviter_id = int(inviter_id)
            else:
                raise serializers.ValidationError("There isn't any user with this referrer code")

        else:
            inviter_id = None

        return User.objects.create_user(user_name=validated_data['user_name'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        inviter_id=inviter_id, )

    def validate_user_name(self, value):
        if value == 'admin':
            raise serializers.ValidationError('Username can not be admin')
        return value

    def validate_email(self, value):
        if 'admin' in value:
            raise serializers.ValidationError('admin can not be in email')
        return value

    def validate_password(self, value):
        if password_validation.validate_password(value):
            raise serializers.ValidationError('the password is easy please use another')
        return value


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = ('name', 'link', 'user_id')

    social_apps = ['telegram', 'instagram', 'youtube', 'twitch', 'discord', 'steam']
    name = serializers.ChoiceField(choices=social_apps)

    def update(self, instance, validated_data):
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    links = SocialMediaSerializer(many=True)
    user_game = serializers.SerializerMethodField()

    # user_games = DailyPlayedGameSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'avatar', 'user_name', 'email', 'bio', 'links', 'hide_button', 'referrer_code', 'user_game')
        extra_kwargs = {
            'email': {'read_only': True},
        }

    def get_user_game(self, obj):
        played_games = obj.user_games.all()
        games = [played_game.game for played_game in played_games]
        return GameSerializer(instance=games, many=True).data

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.hide_button = validated_data.get('hide_button', instance.hide_button)
        instance.save()
        return instance


class UserRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'user_name', 'total_gemyto', 'hide_button')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        hide_button = representation.get('hide_button')
        if hide_button:
            representation.pop('total_gemyto')
        return representation


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    repeat_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Your old password is incorrect')
        return value

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            raise serializers.ValidationError({'error': 'Both old and new passwords are the same'})
        if data['new_password'] != data['repeat_new_password']:
            raise serializers.ValidationError({'error': 'Repetition of password is wrong please try again!'})
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
