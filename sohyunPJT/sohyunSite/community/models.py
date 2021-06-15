from django.db import models
from django.conf import settings


# Create your models here.

class Review(models.Model):
    title = models.CharField(max_length=100)
    movie_title = models.CharField(max_length=50)
    rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 리뷰에 대한 좋아요 기능 추가
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')

class Comment(models.Model):
    # 댓글의 내용
    content = models.CharField(max_length=200)
    # Review 모델 클래스의 id를 가져오기 위해 설정
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # auth 유저의 id를 가져오기 위해 설정
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)