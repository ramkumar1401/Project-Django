from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    def __str__(self):
        return f"{self.title} [{self.isbn}]"

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.username}"
