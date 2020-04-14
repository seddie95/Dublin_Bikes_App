import requests


def getCurrentWeather():
    # weather api url
    url = 'http://api.openweathermap.org/data/2.5/weather?id=7778677&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'

    # use request to call the api and parse the json response
    response = requests.get(url)
    current_weather_data = response.json()
    return current_weather_data


