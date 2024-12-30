from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, AuthorViewSet, GenreViewSet, BorrowRecordViewSet

router = DefaultRouter()
router.register(r'booksapi', BookViewSet, basename='booksapi')
router.register(r'authorsapi', AuthorViewSet, basename='authorsapi')
router.register(r'genresapi', GenreViewSet, basename='genresapi')
router.register(r'borrow-records', BorrowRecordViewSet, basename='borrow-records')

urlpatterns = [
    path('', include(router.urls)),
]
