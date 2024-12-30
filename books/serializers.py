from rest_framework import serializers
from .models import Book, Author, Genre, BorrowRecord
from datetime import datetime

# Author Serializer
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


# Genre Serializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(write_only=True)  # Accepts author name
    genre = serializers.CharField(write_only=True)   # Accepts genre name

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'isbn', 'total_copies', 'available_copies']

    def create(self, validated_data):
        author_name = validated_data.pop('author')  # Get the author name
        genre_name = validated_data.pop('genre')    # Get the genre name

        # Get or create Author and Genre by name
        author, created = Author.objects.get_or_create(name=author_name)
        genre, created = Genre.objects.get_or_create(name=genre_name)

        # Create and return the Book instance
        book = Book.objects.create(author=author, genre=genre, **validated_data)
        return book

    def update(self, instance, validated_data):
        author_name = validated_data.pop('author', None)
        genre_name = validated_data.pop('genre', None)

        if author_name:
            # Get or create Author by name
            author, created = Author.objects.get_or_create(name=author_name)
            instance.author = author

        if genre_name:
            # Get or create Genre by name
            genre, created = Genre.objects.get_or_create(name=genre_name)
            instance.genre = genre

        # Update other fields
        instance.title = validated_data.get('title', instance.title)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.total_copies = validated_data.get('total_copies', instance.total_copies)
        instance.available_copies = validated_data.get('available_copies', instance.available_copies)
        instance.save()
        return instance

class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ['id', 'borrower_name', 'book', 'borrow_date', 'return_date', 'late_fee']

    def create(self, validated_data):
        # Simply create the BorrowRecord without manually handling borrow_date
        borrow_record = BorrowRecord.objects.create(**validated_data)
        return borrow_record