from django.shortcuts import get_object_or_404, render, redirect
from .models import Movie, Rating
from django.views.decorators.http import require_GET, require_POST
from .forms import RatingForm
import random


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies' : movies,
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie,pk=movie_pk)
    ratings = movie.rating_set.all()
    user_ids = list(Rating.objects.filter(movie=movie).values_list('user__id', flat=True))
    rating_form = RatingForm()
    context = {
        'movie' : movie,
        'user_ids': user_ids,
        'ratings': ratings,
        'rating_form': rating_form,
    }
    return render(request, 'movies/detail.html', context)

@require_POST
def create_rating(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rating_form = RatingForm(request.POST)
    if rating_form.is_valid():
        rating = rating_form.save(commit=False)
        rating.movie = movie
        rating.user = request.user
        rating.save()
        return redirect('movies:detail', movie.pk)
    context = {
        'rating_form': rating_form,
        'movie': movie,
        'ratings': movie.rating_set.all(),
    }
    return render(request, 'movies/detail.html', context)

@require_POST
def delete_rating(request, movie_pk, rating_pk):
    if request.user.is_authenticated:
        rating = get_object_or_404(Rating, pk=rating_pk)
        if request.user == rating.user:
            rating.delete()
    return redirect('movies:detail', movie_pk)

def random_movie(request):
    num = random.randint(1, 100)
    movie = get_object_or_404(Movie, pk=num)
    ratings = movie.rating_set.all()
    rating_form = RatingForm()
    context = {
        'movie': movie,
        'ratings': ratings,
        'rating_form': rating_form,
    }
    return render(request, 'movies/detail.html', context)