''' The user serializers '''
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ User serializer for the user objects """
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'phone_number', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        ''' Create and return the user with encrypted password '''
        return get_user_model().objects.create_user(**validated_data)
