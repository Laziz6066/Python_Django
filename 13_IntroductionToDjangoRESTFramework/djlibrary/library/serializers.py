from rest_framework import serializers
from .models import *


class BookSereializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSereializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"