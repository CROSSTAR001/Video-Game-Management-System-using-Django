from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'), 
    path('home/', views.home, name='home'), 
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('games-library/', views.games_library, name='games_library'),
    path('trending-games/', views.trending_games, name='trending_games'),
    path('upcoming-releases/', views.upcoming_releases, name='upcoming_releases'),
    path('awards-top-games/', views.awards_top_games, name='awards_top_games'),
    path('gaming-news/', views.gaming_news, name='gaming_news'),
    path('game-systems/', views.game_systems, name='game_systems'),
    path('history-of-gaming/', views.history_of_gaming, name='history_of_gaming'),
    path('admin/', admin.site.urls)
]
