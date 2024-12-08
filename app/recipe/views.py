''' The Recipe Views '''

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from . import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing recipes.

    This view set provides CRUD operations for recipes, ensuring that
    only authenticated users can access their own recipes. It utilizes
    different serializers based on the action being performed.
    """

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' Retrieve recipes for the authenticated user '''
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        ''' Return the serializer to be used based on the action'''
        if self.action == 'list':
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        ''' Create a new recipe'''
        serializer.save(user=self.request.user)


class TagViewSet(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):
    ''' Manage tags in the database '''
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' Get the tags for the authenticated user '''
        return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
        ):
    ''' Manage the ingredients in the database '''
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' Get the tags for the authenticated user '''
        return self.queryset.filter(user=self.request.user).order_by('-name')
