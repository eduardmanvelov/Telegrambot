from loader import bot
from api.movie_api import search_movies_by_budget
from database.db import log_search

@bot.message_handler(commands=['movie_by_budget'])
def handle_movie_budget_search(message):
    bot.reply_to(message, "Введите минимальный бюджет (например, 1000000):")
    bot.register_next_step_handler(message, process_min_budget)

def process_min_budget(message):
    try:
        min_budget = int(message.text)
        bot.reply_to(message, "Введите максимальный бюджет (например, 5000000):")
        bot.register_next_step_handler(message, process_max_budget, min_budget)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректный бюджет.")
        return

def process_max_budget(message, min_budget):
    try:
        max_budget = int(message.text)
        bot.reply_to(message, "Введите жанр (например, комедия, ужасы):")
        bot.register_next_step_handler(message, process_genre, min_budget, max_budget)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите корректный бюджет.")
        return

def process_genre(message, min_budget, max_budget):
    genre = message.text
    bot.reply_to(message, "Сколько результатов вы хотите вывести?")
    bot.register_next_step_handler(message, process_limit, min_budget, max_budget, genre)

def process_limit(message, min_budget, max_budget, genre):
    try:
        limit = int(message.text)
        movies = search_movies_by_budget(min_budget, max_budget, genre)  # Запрос с диапазоном бюджета
        if movies and 'docs' in movies:  # Проверка на наличие результатов
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
        f"Бюджет: {movie.get('budget', 'Не указан')}\n"  # Отображение бюджета
        f"Постер: {movie.get('poster', 'Нет постера')}"
    )