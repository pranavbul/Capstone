import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from database_setup import DatabaseManager

class WeatherPredictor:
    def __init__(self):
        self.db_manager = DatabaseManager()
    def prepare_features(self, df):
        df['hour'] = df['recorded_at'].dt.hour
        df['day'] = df['recorded_at'].dt.day
        df['month'] = df['recorded_at'].dt.month
        df['temp_lag_1'] = df['temperature'].shift(1)
        df['humidity_lag_1'] = df['humidity'].shift(1)
        df = df.dropna()
        return df
    def get_training_data(self, city_name="Mumbai", days=30):
        if not self.db_manager.connect():
            return None, None
        try:
            data = self.db_manager.get_weather_data(city_name, days)
            cols = ['id', 'city_id', 'temperature', 'feels_like', 'humidity', 
                    'pressure', 'weather_main', 'weather_description', 
                    'wind_speed', 'wind_direction', 'cloud_coverage', 
                    'visibility', 'uv_index', 'recorded_at', 'date_only',
                    'city_name', 'country_code']
            df = pd.DataFrame(data, columns=cols)
            df['recorded_at'] = pd.to_datetime(df['recorded_at'])
            df = self.prepare_features(df)
            features = ['humidity','pressure','wind_speed','cloud_coverage','hour','day','month','temp_lag_1','humidity_lag_1']
            X = df[features]
            y = df['temperature']
            return X, y
        finally:
            self.db_manager.close()
    def train_models(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(),
            'SVR': SVR()
        }
        for name, model in models.items():
            model.fit(X_train_scaled, y_train)
            y_pred = model.predict(X_test_scaled)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print(f"Model: {name}  RMSE: {rmse:.2f}  MAE: {mae:.2f}  R2: {r2:.2f}")
        return models

if __name__ == "__main__":
    predictor = WeatherPredictor()
    X, y = predictor.get_training_data()
    if X is not None and y is not None:
        predictor.train_models(X, y)
