from loader import bot
import sqlite3

def get_history():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM search_history ORDER BY date DESC")
    results = cursor.fetchall()
    conn.close()
    return results

@bot.message_handler(commands=['history'])
def handle_history(message):
    history = get_history()
    if history:
        for record in history:
            bot.send_message(message.chat.id, f"Дата: {record[1]}, Название: {record[2]}, Рейтинг: {record[4]}")
    else:
        bot.send_message(message.chat.id, "История запросов пуста.")