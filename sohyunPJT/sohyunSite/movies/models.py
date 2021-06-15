from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# movies.json파일을 참고했을 때,
# 위쪽 부분의 json파일 부분엔 genre만 모아둔 부분이 있고
# 해당 부분에 "model" : "movies.genre" 라고 적혀있었기 때문에 다음과 같이 작성
class Genre(models.Model):
    name = models.CharField(max_length=50)

# movies.json파일을 참고했을 때,
# 아래쪽 부분의 json파일 부분엔 genre만 모아둔 부분이 있고
# 해당 부분에 "model" : "movies.movie" 라고 적혀있었기 때문에 다음과 같이 작성
class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    def username(self):
        return self.user.username

    def __str__(self):
        return f'{self.movie} | {self.score} | {self.comment}'
