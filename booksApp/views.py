from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")

def create_user(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/users/success')
    return redirect('/')

def main_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'all_books' : Book.objects.all()
    }
    return render(request, 'main_page.html', context)

def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email']) 
        if users_with_email: 
            user = users_with_email[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/users/success') 
        messages.error(request, "Email or password are not right")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect('/')

def create_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books/main_page')
        else:
            user = User.objects.get(id=request.session["user_id"])
            book = Book.objects.create(title=request.POST['title'], description=request.POST
            ['description'], added_by=user)
            book.favorited_by.add(user)
            messages.success(request, "Book created")
            return redirect('/books/main_page')
    return redirect('/books/main_page')

def show_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    books_with_id = Book.objects.filter(id=book_id)
    if len(books_with_id) == 0:
        return redirect('/books/main_page')
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        "one_book": Book.objects.get(id=book_id)
    }
    return render(request, "one_book.html", context)

def update_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = Book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books/main_page')
        else:
            book_to_update = Book.objects.get(id=book_id)
            book_to_update.description = request.POST['description']
            book_to_update.title = request.POST['title']
            book_to_update.save()
            messages.success(request, "Book updated")
            return redirect('/books/main_page')
    return redirect(f'/books/{book_id}')

def delete_book(request, book_id):
    if request.method == "POST":
        book_to_delete = Book.objects.get(id=book_id)
        book_to_delete.delete()
    return redirect('/books/main_page')

def favorite_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    book.favorited_by.add(user)
    # OR You can do:
    # user.favorited_books.add(book)
    return redirect('/books/main_page')

def unfavorite_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    book.favorited_by.remove(user)
    # OR You can do:
    # current_user.giraffes_voted_for.add(one_giraffe)
    return redirect('/books/main_page')

def catch_all(request, url):
    return redirect("/")    