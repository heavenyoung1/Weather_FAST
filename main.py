from fastapi import FastAPI
import uvicorn
import requests

app = FastAPI()

@app.get('/')
def hello():
    # api_key = '4968e589f443bde5a7ebc60af5cb1da0'
    # settings = {'units': 'metric'}
    # data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}')
    # return {'city': city, 'weather': data.json()}
    return 'Hello World'

@app.get('/weather/{city}')
def create_city(city: str):
    api_key = '4968e589f443bde5a7ebc60af5cb1da0'
    settings = {'units': 'metric'}
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    weather_data = response.json()
    if response.status_code == 200:
        return {'city': city, 'weather': weather_data['weather'][0]['main']}
    else:
        return 'ERROR'