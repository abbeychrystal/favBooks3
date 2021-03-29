from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['first_name']) <3:
            errors['first_name'] = "First Name is too short"
        if len(reqPOST['last_name']) <3:
            errors['last_name'] = "Last Name is too short"
        if len(reqPOST['email']) <6:
            errors['email'] = "Email is too short"
        if len(reqPOST['password']) <8:
            errors['password'] = "Password is too short"
        if reqPOST['password'] != reqPOST['pw_conf']:
            errors['match'] = "Password and password confirmation do not match"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):    # test whether a field matches the pattern            
            errors['regex'] = "Invalid email address!"
        USER_WITH_EMAIL = User.objects.filter(email=reqPOST['email'])
        if len(USER_WITH_EMAIL) >= 1:
            errors['dup'] = "Email already taken"
        return errors

class User(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #books_uploaded = a list of books uploaded by a given user
    #favorited_books = a list of books favorited by a given user

class BookManager(models.Manager):
    def book_validator(self, reqPOST):
        errors = {}
        if len(reqPOST['title']) <1:
            errors['title'] = "Title is required"
        if len(reqPOST['description']) <5:
            errors['description'] = "Description must be longer than 5 characters"
        books_with_name = Book.objects.filter(title=reqPOST['title'])
        if len(books_with_name) >= 1:
            errors['unique'] = "Name already taken"
        return errors

class Book(models.Model):
    title = models.TextField()
    description = models.TextField()
    added_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name='favorited_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()