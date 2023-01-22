import sqlite3
import datetime


def creating_db():
    conn = sqlite3.connect('weather_city.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS weather_city(
    city TEXT PRIMARY KEY,
    temp INTEGER,
    wind TEXT,
    pressure TEXT,
    timestamp TEXT);
    """)
    conn.commit()

# def insert_db(city_name, temp, wind, pressure):
#     conn = sqlite3.connect('weather_city.db')
#     cursor = conn.cursor()
#     timestamp = datetime.now()
#     cursor.execute(
#         "INSERT INTO weather_city (city_name, temp, wind, pressure, timestamp) VALUES (?, ?, ?, ?, ?)",
#         (city_name, temp, wind, pressure, timestamp))
#     conn.commit()
