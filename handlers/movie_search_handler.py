from loader import bot
from api.movie_api import search_movies_by_year_and_genre
from database.db import log_search

@bot.message_handler(commands=['movie_search'])
def handle_movie_search(message):
    bot.reply_to(message, "Введите название фильма или сериала:")
    bot.register_next_step_handler(message, process_movie_title)

def process_movie_title(message):
    title = message.text
    bot.reply_to(message, "Введите жанр (например, комедия, ужасы):")
    bot.register_next_step_handler(message, process_movie_genre, title)

def process_movie_genre(message, title):
    genre = message.text
    bot.reply_to(message, "Сколько результатов вы хотите вывести?")
    bot.register_next_step_handler(message, process_movie_limit, title, genre)

def process_movie_limit(message, title, genre):
    try:
        limit = int(message.text)
        bot.reply_to(message, "Введите год выпуска фильма или сериала:")
        bot.register_next_step_handler(message, process_movie_year, title, genre, limit)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректное количество.")
        return

def process_movie_year(message, title, genre, limit):
    try:
        year = int(message.text)
        movies = search_movies_by_year_and_genre(year, genre)  # Здесь вы должны использовать нужный API-запрос
        if movies:
            for movie in movies.get('docs', [])[:limit]:  # Ограничение количества выводимых фильмов
                log_search(movie)  # Логирование поиска
                bot.send_message(message.chat.id, format_movie_info(movie))
        else:
            bot.send_message(message.chat.id, "Фильмы не найдены.")
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректный год.")
        return

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