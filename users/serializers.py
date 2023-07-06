from rest_framework import serializers
from users.models import User, SocialMedia
from game.models import PlayedGame


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
        fields = ('name', 'link')
        
class PlayedGameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PlayedGame
        fields = ('game',)

class UserSerializer(serializers.ModelSerializer):
    links = SocialMediaSerializer(many=True)
    user_games = PlayedGameSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ('avatar', 'user_name', 'email', 'bio', 'links', 'played_game', 'user_games')
        extra_kwargs = {
            'email': {'read_only':True},
        }
        
    def update(self, instance, validated_data):
        links_data = validated_data.pop('links', None)
        #     links_data = validated_data.pop('links')
        # links_data = None
        
        #links = list((instance.links).all())
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.played_game = validated_data.get('played_game', instance.played_game)
        instance.save()
        
        if links_data:
            for link_data in links_data:
                link = SocialMedia.objects.get(pk=link_data['id'])
                link.name = link_data.get('name', link.name)
                link.link = link_data.get('link', link.link)
                link.save()
        
            
        return instance