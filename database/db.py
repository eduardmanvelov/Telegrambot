import sqlite3
from datetime import datetime

def connect_db():
    conn = sqlite3.connect('history.db')
    return conn

def create_history_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY,
        date TEXT,
        title TEXT,
        description TEXT,
        rating REAL,
        year INTEGER,
        genre TEXT
    )
    ''')
    conn.commit()
    conn.close()

def log_search(movie_data):
    conn = connect_db()
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
    INSERT INTO search_history (date, title, description, rating, year, genre)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, movie_data['name'], movie_data.get('description', ''), movie_data['rating'], movie_data['year'], movie_data['genres'][0]['name']))
    conn.commit()
    conn.close()