from fastapi import FastAPI
import uvicorn
import requests
import making_db
from datetime import datetime
import sqlite3

app = FastAPI()

@app.post('/weather/{city}')
def create_city(city: str):
    '''Получение города и запись в БД'''
    api_key = '4968e589f443bde5a7ebc60af5cb1da0'
    units = 'metric'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}'
    response = requests.get(url)
    weather_data = response.json()
    if response.status_code == 200:
        making_db.creating_db()

        conn = sqlite3.connect('weather_city.db')
        cursor = conn.cursor()

        city = city
        temp = weather_data['main']['temp']
        wind = weather_data['wind']['speed']
        pressure = weather_data['main']['pressure']
        timestamp = datetime.now()

        #Запись в БД если такого города ещё нет
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO weather_city (city, temp, wind, pressure, timestamp) VALUES (?, ?, ?, ?, ?)",
                (city, temp, wind, pressure, timestamp))
            conn.commit()
            return 'Данные записаны'

        #Если такой город уже существует, данные обновляются
        except sqlite3.IntegrityError:
            timestamp = datetime.now()
            cursor.execute(
                "UPDATE weather_city SET temp = ?, wind = ?,  pressure = ?, timestamp = ? WHERE city = city",
                (temp, wind, pressure, timestamp))
            conn.commit()
            return 'OK'

    #Проверьте правильность ввода названия
    else:
        return 'Input correct name of city'

@app.get('/last_weather')
def get_weather():
    '''Получить список всех городов и температуры'''
    conn = sqlite3.connect('weather_city.db')
    cursor = conn.cursor()
    (cursor.execute(
        "SELECT city, temp FROM weather_city"
    ))
    city_temp = cursor.fetchall()
    conn.close()
    return {'city_temp': city_temp}

@app.get('/city_stats/{city}')
def get_city_stats(city: str):
    '''Получить все данные города'''
    conn = sqlite3.connect('weather_city.db')
    cursor = conn.cursor()
    (cursor.execute(
        "SELECT * FROM weather_city WHERE city = ?", (city,)))
    city_temp = cursor.fetchall()
    conn.close()
    return {'city_temp': city_temp}
