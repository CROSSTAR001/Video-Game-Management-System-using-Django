from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from datetime import date
import requests
import logging


def login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')  
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('home')
    else:
        return render(request, 'register.html')

@login_required
def home(request):
    return render(request, 'home.html')


def games_library(request):
    return render(request, 'games-library.html')


logger = logging.getLogger(__name__)

def trending_games(request):
    api_url = "https://api.rawg.io/api/games"
    api_key = "ad94ffa4c83a46e185259e62c8d6067a" 
    
    params = {
        "key": api_key,
        "ordering": "-added",
        "page_size": 25,
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        games = response.json().get("results", [])
        logger.info(f"Fetched {len(games)} games from the API")
    except requests.exceptions.RequestException as e:
        games = []
        logger.error(f"Failed to fetch trending games: {e}")

    return render(request, "trending-games.html", {"games": games})

def upcoming_releases(request):
    api_url = "https://api.rawg.io/api/games"
    api_key = "ad94ffa4c83a46e185259e62c8d6067a"

    today = date.today()
    next_year = today.replace(year=today.year + 1)

    params = {
        "key": api_key,
        "dates": f"{today},{next_year}",  
        "ordering": "released",          
        "page_size": 25,               
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        games = response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch upcoming releases: {e}")
        games = []

    return render(request, "upcoming-releases.html", {"games": games})

def awards_top_games(request):
    return render(request, 'awards-top-games.html')

def fetch_related_image(query):
    unsplash_url = "https://api.unsplash.com/search/photos"
    unsplash_key = "lnbGZQhEU_VnkslXTcuY52wQG53C9ohz7vgs69SBrlg" 

    params = {
        "query": query,
        "client_id": unsplash_key,
        "per_page": 1,
    }

    try:
        response = requests.get(unsplash_url, params=params)
        response.raise_for_status()
        results = response.json().get("results")
        if results:
            return results[0]["urls"]["regular"]  
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch related image: {e}")

    return None

def gaming_news(request):
    api_url = "https://newsapi.org/v2/everything"
    api_key = "c2a53e1ce84e45db974077b0beed71a5"

    gaming_keywords = ["gaming", "game", "esports", "console", "PC", "PlayStation", "Xbox", "Nintendo", "Video Games", "Game Awards 2024", "Steam"]

    params = {
        "q": "gaming", 
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": api_key,
        "pageSize": 20, 
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch gaming news: {e}")
        articles = []

    filtered_articles = []
    for article in articles:
        if any(keyword.lower() in article["title"].lower() or keyword.lower() in article.get("description", "").lower() for keyword in gaming_keywords):
            filtered_articles.append(article)

    return render(request, "gaming-news.html", {"articles": filtered_articles})

def game_systems(request):
    return render(request, 'game-systems.html')

def history_of_gaming(request):
    return render(request, 'history-of-gaming.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            with open('contact_messages.txt', 'a') as file:
                file.write(f"Name: {name}, Email: {email}, Message: {message}\n")
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, 'contact.html')

