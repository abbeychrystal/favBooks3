from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('users/create', views.create_user),
    path('users/success', views.main_page),
    path('users/login', views.login),
    path('logout', views.logout),
    path('books/create', views.create_book),
    path('books/main_page', views.main_page),
    path('books/<int:book_id>', views.show_book),
    path('books/<int:book_id>/update', views.update_book),
    path('books/<int:book_id>/delete', views.delete_book),
    path('books/<int:book_id>/favorite', views.favorite_book),
    path('books/<int:book_id>/unfavorite', views.unfavorite_book),
    path('<url>', views.catch_all)
]