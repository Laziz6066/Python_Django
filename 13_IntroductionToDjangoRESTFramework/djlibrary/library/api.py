from django.shortcuts import render
from rest_framework import generics, viewsets
from .serializers import *
from .paginations import *
from django_filters.rest_framework import DjangoFilterBackend


class BookAPISet(viewsets.ModelViewSet):
    """Представление для просмотра информации о книгах, а также для их редактирования, удаления и добавления"""
    queryset = Book.objects.all()
    serializer_class = BookSereializer
    pagination_class = APIListPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        author = self.request.query_params.get('author', None)
        title = self.request.query_params.get('title', None)
        if author:
            queryset = queryset.filter(author__name__icontains=author) | queryset.filter(
                author__last_name__icontains=author)
        if title:
            queryset = queryset.filter(title__icontains=title)
        min_pages = self.request.query_params.get('min_pages', None)
        max_pages = self.request.query_params.get('max_pages', None)
        if min_pages and max_pages:
            queryset = queryset.filter(number_of_pages__range=(min_pages, max_pages))
        elif min_pages:
            queryset = queryset.filter(number_of_pages__gte=min_pages)
        elif max_pages:
            queryset = queryset.filter(number_of_pages__lte=max_pages)
        return queryset


class AuthorAPISet(viewsets.ModelViewSet):
    """Представление для просмотра информации об авторах, а также для их редактирования, удаления и добавления"""
    queryset = Author.objects.all()
    serializer_class = AuthorSereializer
    pagination_class = APIListPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name) | queryset.filter(last_name__icontains=name)
        return queryset