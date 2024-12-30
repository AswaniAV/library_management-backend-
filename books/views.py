from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from .models import Book, Author, Genre, BorrowRecord
from .serializers import BookSerializer, AuthorSerializer, GenreSerializer, BorrowRecordSerializer
from datetime import timedelta
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

# Author ViewSet
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

# Genre ViewSet
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author__name', 'genre__name']  # Enable search by author and genre

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    # Action to return a book and calculate late fee
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrow_record = self.get_object()
        
        # Get return date from request data
        return_date = request.data.get('return_date')
        if return_date:
            borrow_record.return_date = return_date
            borrow_record.calculate_late_fee()  # Calculate late fee
            borrow_record.save()

            return Response({
                'borrower_name': borrow_record.borrower_name,
                'book_title': borrow_record.book.title,
                'borrow_date': borrow_record.borrow_date,
                'return_date': borrow_record.return_date,
                'late_fee': borrow_record.late_fee
            })
        else:
            return Response({'error': 'Return date is required'}, status=status.HTTP_400_BAD_REQUEST)
       