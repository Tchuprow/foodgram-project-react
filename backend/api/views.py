from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipe.models import Favorite, Ingredient, Recipe, ShopingList, Tag
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.filters import RecipeFilter
from api.paginators import PagePaginator
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CustomUserSerializer, FavoriteSerializer,
                             FollowListSerializer, FollowSerializer,
                             IngredientSerializer, RecipeListSerializer,
                             RecipeSerializer, ShopingListSerializer,
                             TagSerializer)
from users.models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)


class FollowListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PagePaginator

    def get(self, request):
        serializer = FollowListSerializer(
            self.paginate_queryset(
                User.objects.filter(following__user=request.user)),
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)


class FollowViewSet(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = PagePaginator    
    def post(self, request, user_id):
        serializer = FollowSerializer(
            data={'user': request.user.id, 'following': user_id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        following = get_object_or_404(User, id=user_id)
        try:
            subscription = Follow.objects.get(user=user, following=following)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(
                'Вы уже отписались от этого автора',
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagsViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = PagePaginator

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=("post",),
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=("post",),
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShopingListSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShopingList)

    @action(detail=False, methods=("get",),
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        filename = f'{request.user.username}_shopping_list.txt'
        shopping_list = []
        ingredients = Ingredient.objects.filter(
            amounts__recipe__shoping_list__user=request.user
        ).values(
            'name',
            measurement=F('measurement_unit')
        ).annotate(amount=Sum('amounts__amount'))

        for ing in ingredients:
            shopping_list.append(
                f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
            )
        shopping_list.append('\nПосчитано в Foodgram')
        shopping_list = '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
