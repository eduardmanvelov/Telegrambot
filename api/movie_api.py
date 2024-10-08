import requests
from config import MOVIE_API_KEY

BASE_URL = "https://api.kinopoisk.dev/v1.4/movie"

def search_movies_by_year_and_genre(year, genre):
    params = {
        'year': year,
        'genres.name': genre
    }
    headers = {
        'X-API-KEY': MOVIE_API_KEY
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def search_movies_by_rating(rating_min, rating_max):
    params = {
        'rating.imdb': f"{rating_min}-{rating_max}"
    }
    headers = {
        'X-API-KEY': MOVIE_API_KEY
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def search_movies_by_budget(min_budget, max_budget, genre):
    params = {
        'budget': f"{min_budget}-{max_budget}",
        'genre': genre
    }
    headers = {
        'X-API-KEY': MOVIE_API_KEY
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None