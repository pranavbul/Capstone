import requests
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPIClient:
    def __init__(self):
        self.api_key = os.getenv('e180d49478164e7499901597e7d02c1d')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not set.")

    def get_current_weather(self, city_name, country_code=None):
        try:
            location = city_name
            if country_code:
                location += f",{country_code}"
            url = f"{self.base_url}/weather"
            params = {'q': location, 'appid': self.api_key, 'units': 'metric'}
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            weather_data = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'wind_direction': data.get('wind', {}).get('deg', 0),
                'cloud_coverage': data.get('clouds', {}).get('all', 0),
                'visibility': data.get('visibility', 10000),
                'uv_index': None,
                'city_info': {
                    'name': data['name'],
                    'country': data['sys']['country'],
                    'latitude': data['coord']['lat'],
                    'longitude': data['coord']['lon']
                }
            }
            return weather_data
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_uv_index(self, latitude, longitude):
        # Endpoint for UV index is paid, typically skip or simulate in free plans
        return 0

    def get_weather_with_uv(self, city_name, country_code=None):
        weather_data = self.get_current_weather(city_name, country_code)
        if weather_data:
            uv_index = self.get_uv_index(weather_data['city_info']['latitude'], weather_data['city_info']['longitude'])
            weather_data['uv_index'] = uv_index
        return weather_data

    def test_api_connection(self):
        try:
            test_data = self.get_current_weather("London", "GB")
            return bool(test_data)
        except:
            return False

if __name__ == "__main__":
    api_client = WeatherAPIClient()
    if api_client.test_api_connection():
        print("API key works!")
    else:
        print("API test failed.")
