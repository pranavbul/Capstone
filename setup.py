import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            self.cursor = self.connection.cursor()
            print("Connected to PostgreSQL database successfully!")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False

    def create_tables(self):
        drop_tables_query = '''
        DROP TABLE IF EXISTS weather_data CASCADE;
        DROP TABLE IF EXISTS cities CASCADE;
        '''
        create_cities_table = '''
        CREATE TABLE cities (
            id SERIAL PRIMARY KEY,
            city_name VARCHAR(100) NOT NULL,
            country_code VARCHAR(5) NOT NULL,
            latitude DECIMAL(10, 8),
            longitude DECIMAL(11, 8),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(city_name, country_code)
        );
        '''
        create_weather_table = '''
        CREATE TABLE weather_data (
            id SERIAL PRIMARY KEY,
            city_id INTEGER REFERENCES cities(id),
            temperature DECIMAL(5, 2),
            feels_like DECIMAL(5, 2),
            humidity INTEGER,
            pressure INTEGER,
            weather_main VARCHAR(50),
            weather_description VARCHAR(100),
            wind_speed DECIMAL(5, 2),
            wind_direction INTEGER,
            cloud_coverage INTEGER,
            visibility INTEGER,
            uv_index DECIMAL(4, 2),
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_only DATE GENERATED ALWAYS AS (recorded_at::date) STORED
        );
        '''
        create_indexes = '''
        CREATE INDEX idx_weather_city_date ON weather_data(city_id, date_only);
        CREATE INDEX idx_weather_recorded_at ON weather_data(recorded_at);
        CREATE INDEX idx_cities_name_country ON cities(city_name, country_code);
        '''
        try:
            self.cursor.execute(drop_tables_query)
            self.cursor.execute(create_cities_table)
            self.cursor.execute(create_weather_table)
            self.cursor.execute(create_indexes)
            self.connection.commit()
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.connection.rollback()

    def insert_city(self, city_name, country_code, latitude=None, longitude=None):
        try:
            query = '''
            INSERT INTO cities (city_name, country_code, latitude, longitude)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city_name, country_code) DO UPDATE SET
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude
            RETURNING id;
            '''
            self.cursor.execute(query, (city_name, country_code, latitude, longitude))
            city_id = self.cursor.fetchone()[0]
            self.connection.commit()
            return city_id
        except Exception as e:
            print(f"Error inserting city: {e}")
            self.connection.rollback()
            return None

    def insert_weather_data(self, city_id, weather_data):
        try:
            query = '''
            INSERT INTO weather_data (
                city_id, temperature, feels_like, humidity, pressure,
                weather_main, weather_description, wind_speed, wind_direction,
                cloud_coverage, visibility, uv_index
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''
            self.cursor.execute(query, (
                city_id,
                weather_data.get('temperature'),
                weather_data.get('feels_like'),
                weather_data.get('humidity'),
                weather_data.get('pressure'),
                weather_data.get('weather_main'),
                weather_data.get('weather_description'),
                weather_data.get('wind_speed'),
                weather_data.get('wind_direction'),
                weather_data.get('cloud_coverage'),
                weather_data.get('visibility'),
                weather_data.get('uv_index')
            ))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error inserting weather data: {e}")
            self.connection.rollback()
            return False

    def get_weather_data(self, city_name, days=30):
        try:
            query = '''
            SELECT wd.*, c.city_name, c.country_code
            FROM weather_data wd
            JOIN cities c ON wd.city_id = c.id
            WHERE c.city_name = %s
            AND wd.recorded_at >= NOW() - INTERVAL '%s days'
            ORDER BY wd.recorded_at DESC;
            '''
            self.cursor.execute(query, (city_name, days))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving weather data: {e}")
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed")

if __name__ == "__main__":
    db = DatabaseManager()
    if db.connect():
        db.create_tables()
        # Optional: Insert initial city
        city_id = db.insert_city("Mumbai", "IN", 19.0760, 72.8777)
        if city_id:
            print(f"Mumbai city inserted with ID: {city_id}")
        db.close()
