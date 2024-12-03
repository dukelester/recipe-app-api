'''
Serializers for the APIS
'''

from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    ''' Serializer for the Recipe '''
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_in_minutes',
            'price', 'link', 'description',
                ]
        read_only_fields = ['id']
