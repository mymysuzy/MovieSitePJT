from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/comments/', views.create_comment, name='create_comment'),
    path('<int:review_pk>/comments/<int:comment_pk>', views.delete_comment, name='delete_comment'),
    # 좋아요 기능
    path('<int:review_pk>/like/', views.like, name='like'),
]