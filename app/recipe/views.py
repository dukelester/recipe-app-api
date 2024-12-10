''' The Recipe Views '''

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Recipe, Tag, Ingredient
from . import serializers


class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    ''' The Base view for the viewsets '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ''' Get the tags for the authenticated user '''
        return self.queryset.filter(user=self.request.user).order_by('-name')


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
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        ''' Create a new recipe'''
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload_image')
    def upload_image(self, request, pk=None):
        ''' Upload the image to recipe '''
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(BaseRecipeAttrViewSet):
    ''' Manage tags in the database '''
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    ''' Manage the ingredients in the database '''
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
