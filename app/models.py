from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    date=models.DateField()
    isbn=models.CharField(max_length=13,unique=True)
    copies=models.IntegerField(default=1)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned = models.BooleanField(default=False)
    
class HelpRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)