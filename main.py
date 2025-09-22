import time
from database_setup import DatabaseManager
from weather_api import WeatherAPIClient
from data_collector import WeatherDataCollector
from weather_visualization import WeatherVisualizer
from weather_ml_prediction import WeatherPredictor

def main():
    db_manager = DatabaseManager()
    if db_manager.connect():
        db_manager.create_tables()
        db_manager.close()
    api = WeatherAPIClient()
    if api.test_api_connection():
        print("API ok, continuing.")
    collector = WeatherDataCollector()
    collector.collect_weather_data("Mumbai", "IN")
    viz = WeatherVisualizer()
    df = viz.get_data_for_visualization("Mumbai", 30)
    if df is not None and not df.empty:
        viz.create_temperature_trend(df)
        viz.create_interactive_plot(df)
    predictor = WeatherPredictor()
    X, y = predictor.get_training_data("Mumbai", 30)
    if X is not None:
        predictor.train_models(X, y)

if __name__ == "__main__":
    main()
