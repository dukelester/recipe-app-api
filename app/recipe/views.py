''' The Recipe Views '''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from . import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    '''' View for managing the recipe APIs'''
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
