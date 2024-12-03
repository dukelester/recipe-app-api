'''
Serializers for the APIS
'''

from rest_framework import serializers

from core.models import Recipe, Tag


class RecipeSerializer(serializers.ModelSerializer):
    ''' Serializer for the Recipe '''
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_in_minutes',
            'price', 'link', 'description',
                ]
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    ''' The recipe details serializer '''
    class Meta(RecipeSerializer.Meta):
        class Meta(RecipeSerializer.Meta):
            """Meta class for the RecipeSerializer.

            This class inherits from the Meta class of RecipeSerializer
            and specifies the fields to be included in the serialized output.
            same fields are used consistently across different serializers.

            Attributes:
                fields (tuple): The fields to be included in the
                serialized output.
            """
            fields = RecipeSerializer.Meta.fields


class TagSerializer(serializers.ModelSerializer):
    ''' The Tags serializer '''
    class Meta:
        ''' Serializer for tags '''
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
