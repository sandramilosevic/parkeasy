from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    # password is never returned in response
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'password', 'user_type', 'phone_number']
    # create is called when user sends POST request for registration

    def create(self, validated_data):
        # automatically hashes password before saving to database
        user = User.objects.create_user(**validated_data)
        return user


class UserSerialized(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'phone_number']
