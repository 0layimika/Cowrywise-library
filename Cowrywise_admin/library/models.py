from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField()
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)
class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    publisher = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    availability = models.BooleanField(default=True)

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateField(auto_now_add=True)
    return_data = models.DateField()
