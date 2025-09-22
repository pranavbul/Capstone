import schedule
import time
from datetime import datetime
from weather_api import WeatherAPIClient
from database_setup import DatabaseManager

class WeatherDataCollector:
    def __init__(self):
        self.api_client = WeatherAPIClient()
        self.db_manager = DatabaseManager()
        
    def collect_weather_data(self, city_name="Mumbai", country_code="IN"):
        if not self.db_manager.connect():
            return False
        try:
            weather_data = self.api_client.get_weather_with_uv(city_name, country_code)
            if weather_data:
                city_id = self.db_manager.insert_city(
                    weather_data['city_info']['name'],
                    weather_data['city_info']['country'],
                    weather_data['city_info']['latitude'],
                    weather_data['city_info']['longitude']
                )
                if city_id:
                    success = self.db_manager.insert_weather_data(city_id, weather_data)
                    if success:
                        print(f"Weather data collected for {city_name} at {datetime.now()}")
                        return True
        except Exception as e:
            print(f"Error collecting weather data: {e}")
        finally:
            self.db_manager.close()
        return False

    def start_scheduled_collection(self):
        schedule.every().hour.do(self.collect_weather_data)
        print("Started scheduled weather data collection...")
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    collector = WeatherDataCollector()
    collector.start_scheduled_collection()
