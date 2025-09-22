import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from database_setup import DatabaseManager

class WeatherVisualizer:
    def __init__(self):
        self.db_manager = DatabaseManager()
    def get_data_for_visualization(self, city_name="Mumbai", days=30):
        if not self.db_manager.connect():
            return None
        try:
            data = self.db_manager.get_weather_data(city_name, days)
            cols = ['id', 'city_id', 'temperature', 'feels_like', 'humidity', 
                    'pressure', 'weather_main', 'weather_description', 
                    'wind_speed', 'wind_direction', 'cloud_coverage', 
                    'visibility', 'uv_index', 'recorded_at', 'date_only',
                    'city_name', 'country_code']
            df = pd.DataFrame(data, columns=cols)
            df['recorded_at'] = pd.to_datetime(df['recorded_at'])
            return df
        finally:
            self.db_manager.close()
    def create_temperature_trend(self, df):
        plt.plot(df['recorded_at'], df['temperature'], label="Temperature (C)")
        plt.plot(df['recorded_at'], df['feels_like'], label="Feels Like (C)", alpha=0.7)
        plt.title("Temperature Trend (Last 30 Days)")
        plt.xlabel("Date")
        plt.ylabel("Temperature (Celsius)")
        plt.grid(alpha=0.3)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("temperature_trend.png")
        plt.show()
    def create_interactive_plot(self, df):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['recorded_at'], y=df['temperature'],
                                 mode='lines+markers', name='Temperature'))
        fig.add_trace(go.Scatter(x=df['recorded_at'], y=df['humidity'],
                                 mode='lines+markers', name='Humidity (%)', yaxis="y2"))
        fig.update_layout(
            title="Temperature and Humidity (Last 30 Days)",
            xaxis_title="Date",
            yaxis=dict(title='Temperature (C)', side='left'),
            yaxis2=dict(title='Humidity (%)', side='right', overlaying='y'),
            hovermode='x unified'
        )
        fig.write_html("interactive_weather_plot.html")
        fig.show()

if __name__ == "__main__":
    viz = WeatherVisualizer()
    df = viz.get_data_for_visualization()
    if df is not None and not df.empty:
        viz.create_temperature_trend(df)
        viz.create_interactive_plot(df)
