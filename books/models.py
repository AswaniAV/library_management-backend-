from django.db import models
from django.utils.timezone import now
from datetime import timedelta, datetime

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)   
    isbn = models.CharField(max_length=13, unique=True)         
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    borrower_name = models.CharField(max_length=255)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrow_date = models.DateField(default=datetime.now)  # Default to the current date
    return_date = models.DateField(null=True, blank=True)
    late_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.borrower_name} borrowed {self.book.title}"

    def calculate_late_fee(self):
        # Define the borrowing period (14 days)
        borrowing_period = timedelta(days=14)
        
        # Calculate due date (borrow_date + 14 days)
        due_date = self.borrow_date + borrowing_period
        
        # Check if the return_date is later than the due date
        if self.return_date and self.return_date > due_date:
            late_days = (self.return_date - due_date).days
            self.late_fee = late_days * 2  # Example: $2 per late day
        else:
            self.late_fee = 0.00  # No late fee if returned on time

    def save(self, *args, **kwargs):
        # Avoid recursion by only calculating late fee if it's a new record or updated return_date
        if not self.id or self.return_date != self.__class__.objects.get(id=self.id).return_date:
            self.calculate_late_fee()
        
        super().save(*args, **kwargs)

