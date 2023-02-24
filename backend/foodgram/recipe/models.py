from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=256
    )
    units = models.CharField(
        verbose_name='Единица измерения',
        max_length=64, blank=True
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'units'],
                name='unique ingredient',
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.units}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тега',
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=7,
    )
    slug = models.SlugField(
        verbose_name='Адрес тега',
        unique=True,
        max_length=200,
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def _str_(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        max_length=1000,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(
            MinValueValidator(
                1,
                message='Время приготовления не может быть меньше минуты.'
            ),
        ),
    )
    pub_date = models.DateField(
        verbose_name='Время публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='amounts',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='amounts',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=(
            MinValueValidator(
                1,
                message='Количество не может быть меньше 1.'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Amount ingredient'
        verbose_name_plural = 'Amount ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique amount'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь с избранным рецептом',
        related_name='favorites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранный рецепт',
        related_name='favorites',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique favorite'
            )
        ]


class ShopingList(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='shoping_list',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='shoping_list',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'shoping_list'
        verbose_name_plural = 'shoping_lists'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique shoping list'
            )
        ]
