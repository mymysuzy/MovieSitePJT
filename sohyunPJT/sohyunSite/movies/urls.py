from django.contrib import admin
from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/rating/', views.create_rating, name='create_rating'),
    path('<int:movie_pk>/rating/<int:rating_pk>', views.delete_rating, name='delete_rating'),
    path('random_movie/', views.random_movie, name='random_movie'),
]