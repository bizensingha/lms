from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Book, HelpRequest,Profile,BorrowedBook
# Create your views here.
def register(request):
    if request.method=="POST":
        name=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        print(name,email,password1,password2)
        if password1!=password2:
            return redirect("register")
        user=User.objects.create_user(username=name,email=email,password=password2)
        user.save()
        Profile.objects.create(user=user)
        return redirect("login")
    return render(request,"register.html",{})
def loginpage(request):
    if request.method=="POST":
        name=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=name,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
    return render(request,"login.html",{})
def home(request):
    return render(request,"base.html",{})
def dashboard_view(request):
    total_books = Book.objects.count()
    return render(request, 'dashboard.html', {'total_books': total_books})
def books_view(request):
    books=Book.objects.all()
    return render(request, 'booklist.html', {'books':books})
def booklist(request):
    query = request.GET.get('query')
    if query:
        books = Book.objects.filter(title=query)
    else:
        books = Book.objects.all()
    return render(request, 'books.html', {'books': books})
    # return render(request, 'books.html', {'books':books})

def welcome(request):
    
    return render(request, 'welcome.html', {})
def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})

def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile_pic = request.FILES.get('profile_pic')

        user = request.user
        user.username = username
        user.email = email
        user.save()

        profile =get_object_or_404(Profile, user=request.user)
        if phone_number:
            profile.phone_number = phone_number
        if profile_pic:
            profile.profile_pic = profile_pic
        profile.save()
        # Update the session with the new username
        # update_session_auth_hash(request, user)
        # messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')
    return render(request, 'update.html')

def add_book(request):
    if request.method == 'POST':
        # Extract data from the request
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        isbn = request.POST.get('isbn')
        copies = request.POST.get('copies')

        # Validate and create the book instance
        if title and author and published_date and isbn and copies:
            book = Book.objects.create(
                title=title,
                author=author,
                date=published_date,
                isbn=isbn,
                copies=copies
            )
            book.save()
            # Optionally, add success message or other logic
            return redirect('books')  # Redirect to the books list page after adding a book

    return render(request, 'addbook.html')
def log_out(request):
    logout(request)
    return redirect("login")

def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.copies > 0:
        BorrowedBook.objects.create(
            user=request.user,
            book=book,
            due_date=timezone.now() + timedelta(days=14)  # Set due date to 2 weeks from now
        )
        book.copies -= 1
        book.save()
        return redirect('books')  # Redirect to the books list page or another page
    else:
        # Handle the case where no copies are available
        return redirect('books')
    
def borrowed_books(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, returned=False)
    
    return render(request, 'borrowedbooks.html', {'borrowed_books': borrowed_books})

def return_book(request, borrow_id):
    borrow = get_object_or_404(BorrowedBook, id=borrow_id, user=request.user)
    if request.method == 'POST':
        borrow.returned = True
        borrow.book.copies += 1
        borrow.book.save()
        borrow.save()
        return redirect('borrowed_books')
    return redirect('dashboard')
def renew_loan(request, borrow_id):
    borrow = get_object_or_404(BorrowedBook, id=borrow_id, user=request.user)
    
    if borrow.returned:
        messages.error(request, 'This book has already been returned.')
    else:
        # Extend the due date by 7 days (or any other logic you prefer)
        borrow.due_date += timedelta(days=7)
        borrow.save()
    return redirect('borrowed_books')

def help_request(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            help_request = HelpRequest.objects.create(user=request.user, message=message, submitted_at=timezone.now())
            messages.success(request, 'Your help request has been submitted.')
            return redirect('dashboard')  # Redirect to dashboard or any other page after submission
        else:
            messages.error(request, 'Please enter a message.')
    
    return render(request, 'dashboard.html')
def requests_view(request):
    help_requests = HelpRequest.objects.all()  # Retrieve all help requests
    return render(request, 'requests.html', {'help_requests': help_requests})

    # return render(request, 'borrowedbooks.html', {'borrow': borrow})