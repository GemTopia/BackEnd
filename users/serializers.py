from rest_framework import serializers
from users.models import User

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only':True},
        }

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['username'], 
                                        email=validated_data['email'], 
                                        password=validated_data['password'])

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('Username can not be admin')
        return value

    def validate_username(self, value):
        if 'admin' in value:
            raise serializers.ValidationError('admin can not be in email')
