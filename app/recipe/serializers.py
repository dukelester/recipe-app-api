'''
Serializers for the APIS
'''

from rest_framework import serializers

from core.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    ''' The Tags serializer '''
    class Meta:
        ''' Serializer for tags '''
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    ''' Serializer for the Recipe '''
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_in_minutes',
            'price', 'link', 'description', 'tags',
                ]
        read_only_fields = ['id']

    def _get_or_create_tag(self, tags, recipe):
        ''' Create or get a tag'''
        auth_user = self.context['request'].user
        for tag in tags:
            tag_object, created = Tag.objects.get_or_create(
                user=auth_user,**tag
            )
            recipe.tags.add(tag_object)

    def create(self, validated_data):
        ''' Create a recipe '''
        tags_data = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tag(tags_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        ''' Update the recipe'''
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tag(tags, instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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
