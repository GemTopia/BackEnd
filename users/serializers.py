from rest_framework import serializers
from users.models import User

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user_name', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only':True},
            }

    def create(self, validated_data):
        print("89898989988899")
        print(validated_data)
        return User.objects.create_user(user_name=validated_data['user_name'],
                                        email=validated_data['email'], 
                                        password=validated_data['password'])

    def validate_username(self, value):
        if value == 'admin':
            raise serializers.ValidationError('Username can not be admin')
        return value

    def validate_username(self, value):
        if 'admin' in value:
            raise serializers.ValidationError('admin can not be in email')
