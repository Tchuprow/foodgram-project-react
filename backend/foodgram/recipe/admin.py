from django.contrib import admin

from .models import (Ingredient, Tag, Recipe,
                     IngredientAmount, Favorite, ShopingList)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'units',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'amount_favorites',)
    list_filter = ('name', 'author', 'tags',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    @staticmethod
    def amount_favorites(obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    empty_value_display = '-пусто-'


admin.site.register(IngredientAmount)
admin.site.register(Favorite)
admin.site.register(ShopingList)
