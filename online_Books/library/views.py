from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Book, BorrowedBook

def home(request):
    return render(request, 'library/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sign up successful! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'library/signup.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('home')

@login_required
def dashboard(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user, return_date__isnull=True)

    search_query = request.GET.get('q', '')
    if search_query:
        available_books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(category__name__icontains=search_query),
            quantity__gt=0
        ).distinct()
    else:
        available_books = Book.objects.filter(quantity__gt=0)

    context = {
        'borrowed_books': borrowed_books,
        'available_books': available_books,
        'search_query': search_query,
    }
    return render(request, 'library/dashboard.html', context)

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if book.quantity > 0:
        BorrowedBook.objects.create(user=request.user, book=book)
        book.quantity -= 1
        book.save()
        messages.success(request, f"You borrowed: {book.title}")
    else:
        messages.error(request, f"Sorry, {book.title} is not available right now.")
    return redirect('dashboard')

@login_required
def return_book(request, borrow_id):
    borrowed_book = get_object_or_404(BorrowedBook, pk=borrow_id, user=request.user)
    borrowed_book.return_date = timezone.now().date()
    borrowed_book.save()
    book = borrowed_book.book
    book.quantity += 1
    book.save()
    messages.success(request, f"You returned: {book.title}")
    return redirect('dashboard')

def about(request):
    return render(request, 'library/about.html')

def help_page(request):
    return render(request, 'library/help.html')
