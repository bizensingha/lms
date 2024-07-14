from django.contrib import admin
from .models import Book,Profile,BorrowedBook,HelpRequest
# Register your models here.
admin.site.register(Book)
admin.site.register(Profile)
admin.site.register(BorrowedBook)
admin.site.register(HelpRequest)

