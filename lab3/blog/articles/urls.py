from django.urls import path
from . import views

urlpatterns = [
    path('', views.archive, name='archive'),
    path('article/<int:article_id>/', views.get_article, name='get_article'),
    path('article/new/', views.create_post, name='create_post'),
]