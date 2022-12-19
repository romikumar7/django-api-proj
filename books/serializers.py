from rest_framework import serializers
from books.models import Book, Author, Genre

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
      
class BookListSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    genre = serializers.StringRelatedField()
    class Meta:
        model = Book
        fields = ['title', 'pageCount', 'releaseDate', 'authors', 'genre']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'pageCount', 'releaseDate', 'authors', 'genre']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'