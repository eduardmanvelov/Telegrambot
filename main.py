from loader import bot
from database.db import create_history_table

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я ваш помощник по поиску фильмов и сериалов. "
        "Вы можете использовать команды:\n"
        "● /movie_search — поиск фильма/сериала по названию;\n"
        "● /movie_by_rating — поиск фильмов/сериалов по рейтингу;\n"
        "● /low_budget_movie — поиск фильмов/сериалов с низким бюджетом;\n"
        "● /high_budget_movie — поиск фильмов/сериалов с высоким бюджетом;\n"
        "● /history — возможность просмотра истории запросов."
    )

if __name__ == "__main__":
    create_history_table()
    bot.polling(none_stop=True)