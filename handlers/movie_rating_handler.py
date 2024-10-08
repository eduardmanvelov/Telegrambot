from loader import bot
from api.movie_api import search_movies_by_rating
from database.db import log_search

@bot.message_handler(commands=['movie_by_rating'])
def handle_movie_rating_search(message):
    bot.reply_to(message, "Введите минимальный рейтинг (например, 7):")
    bot.register_next_step_handler(message, process_movie_rating)

def process_movie_rating(message):
    try:
        min_rating = float(message.text)
        bot.reply_to(message, "Введите жанр (например, комедия, ужасы):")
        bot.register_next_step_handler(message, process_movie_genre, min_rating)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректный рейтинг.")
        return

def process_movie_genre(message, min_rating):
    genre = message.text
    bot.reply_to(message, "Сколько результатов вы хотите вывести?")
    bot.register_next_step_handler(message, process_movie_limit, min_rating, genre)

def process_movie_limit(message, min_rating, genre):
    try:
        limit = int(message.text)
        movies = search_movies_by_rating(min_rating, genre)  # Запрос к API для поиска по рейтингу и жанру
        if movies:
            for movie in movies.get('docs', [])[:limit]:  # Ограничение количества выводимых фильмов
                log_search(movie)  # Логирование поиска
                bot.send_message(message.chat.id, format_movie_info(movie))
        else:
            bot.send_message(message.chat.id, "Фильмы не найдены.")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректное количество.")

def format_movie_info(movie):
    return (
        f"Название: {movie['name']}\n"
        f"Описание: {movie.get('description', 'Нет описания')}\n"
        f"Рейтинг: {movie.get('rating', 'Нет рейтинга')}\n"
        f"Год: {movie.get('year', 'Не указан')}\n"
        f"Жанр: {', '.join(g['name'] for g in movie['genres'])}\n"
        f"Возрастной рейтинг: {movie.get('ageRating', 'Не указан')}\n"
        f"Постер: {movie.get('poster', 'Нет постера')}"
    )