from rest_framework import serializers
from users.models import User, SocialMedia
from game.models import PlayedGame
from game.serializers import DailyPlayedGameSerializer


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_name', 'email', 'password',)
        extra_kwargs = {
            'password': {'write_only':True},
        }

    def create(self, validated_data, referrer_code):
        if referrer_code:
            inviter_id = User.objects.filter(referrer_code=referrer_code).values_list('id', flat=True).first()
            if inviter_id is not None:
                inviter_id = int(inviter_id)
            else:
                raise "There isn't any user with this referrer code"

        else:
            inviter_id=None

        return User.objects.create_user(user_name=validated_data['user_name'],
                                        email=validated_data['email'], 
                                        password=validated_data['password'],
                                        inviter_id=inviter_id,)

    def validate_user_name(self, value):
        if value == 'admin':
            raise serializers.ValidationError('Username can not be admin')
        return value

    def validate_email(self, value):
        if 'admin' in value:
            raise serializers.ValidationError('admin can not be in email')
        return value

class SocialMediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SocialMedia
        fields = ('name', 'link','user_id')

    social_apps=['telegram','instagram','youtube','twitch','discord','steam']
    name=serializers.ChoiceField(choices=social_apps)

    
    def update(self, instance, validated_data):
        instance.link = validated_data.get('link', instance.link)
        instance.save()
        return instance 

        
        
class UserSerializer(serializers.ModelSerializer):
    links = SocialMediaSerializer(many=True)
    user_games = DailyPlayedGameSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('avatar', 'user_name', 'email', 'bio', 'links', 'hide_button','referrer_code','user_games')
        extra_kwargs = {
            'email': {'read_only':True},
        }
        
        
    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.hide_button = validated_data.get('hide_button', instance.hide_button)
        instance.save()
        return instance