import requests

API_KEY = "7f67693a4c8e1040427834b0c891283d"
CITY_NAME = "St petersburg"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        print(f"Weather in {city}: {weather}")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
    else:
        print(f"Error: {data['message']}")


get_weather(CITY_NAME)

