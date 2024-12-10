''' admin section '''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users """
    ordering = ['id']
    list_display = ['email', 'name', 'phone_number']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'phone_number', 'password1', 'password2',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
    )


admin.site.register(models.User, UserAdmin)


class RecipeDisplay(admin.ModelAdmin):
    """ Define the admin pages for Recipe """
    ordering = ['id']
    list_display = [
        'user', 'title', 'description', 'time_in_minutes',
        'price', 'get_tags', 'get_ingredients']

    def get_tags(self, obj):
        ''' The tags '''
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

    def get_ingredients(self, obj):
        ''' The ingredients '''
        return ", ".join([ingredient.name for ingredient in obj.ingredients.all()])
    get_ingredients.short_description = 'Ingredients'


admin.site.register(models.Recipe, RecipeDisplay)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
