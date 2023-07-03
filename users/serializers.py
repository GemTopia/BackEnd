from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_name', 'email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data, referrer_code):
        if referrer_code:
            inviter_id = User.objects.filter(referrer_code=referrer_code).values_list('id', flat=True).first()
            if inviter_id is not None:
                inviter_id = int(inviter_id)
            else:
                raise "There isn't any user with this referrer code"

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
