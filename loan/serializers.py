from rest_framework import serializers
from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object """

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True, 'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """create a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user