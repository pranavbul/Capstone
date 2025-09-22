
# Weather Data Analytics Project

[![GitHub Repository](https://img.shields.io/badge/GitHub-Weather%20Analytics-blue?logo=github)](https://github.com/yourusername/weather-analytics-project)

---

## Overview

This project provides a comprehensive weather data analytics system that includes:

- Live weather data collection from OpenWeatherMap API
- Storage in a PostgreSQL database with optimized schema
- Visualization of the last 30 days of weather data per city
- Basic machine learning models for weather forecasting

The project is modular, production-ready, and easily extendable.

---

## Features

- Fetches and stores live weather data automatically
- Maintains a relational database for cities and weather parameters
- Generates insightful visualizations (trend charts, dashboards, interactive plots)
- Trains and evaluates ML models (Linear Regression, Random Forest, SVR) for temperature prediction
- Fully documented code with environment configuration and usage guidelines

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- An OpenWeatherMap API key (free tier allows 1000 calls/day)

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/weather-analytics-project.git
   cd weather-analytics-project
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Rename `.env.example` to `.env` and update it with your API key and PostgreSQL credentials.

5. Initialize the database:

   ```
   python database_setup.py
   ```

6. Run the main application:

   ```
   python main.py
   ```

---

## Project Structure

- `database_setup.py` — PostgreSQL database connection and schema creation  
- `weather_api.py` — Client for live weather data fetching with error handling  
- `data_collector.py` — Automated scheduling for continuous weather data collection  
- `weather_visualization.py` — Generate insightful visual and interactive weather charts  
- `weather_ml_prediction.py` — Train and evaluate machine learning models for forecasting  
- `main.py` — Orchestrates setup, collection, visualization, and forecasting workflow  
- `requirements.txt` — Python package dependencies list  
- `.env.example` — Environment variable template  

---

## Machine Learning Models

Trained models for temperature forecasting:

| Model               | Description                |
| ------------------- | --------------------------|
| Linear Regression   | Baseline linear modeling   |
| Random Forest       | Ensemble tree-based model  |
| Support Vector Reg. | Kernel-based regression    |

Models are trained using features such as humidity, pressure, wind speed, datetime information, and lag variables from historical data.

---

## Visualizations

- Temperature trend over last 30 days  
- Multi-parameter weather dashboard  
- Interactive Plotly graphs for temperature and humidity  
- ML prediction error plots

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests with improvements or fixes.

---

## License

This project is released under the MIT License.

---

## Contact

Project maintained by [Your Name] - [Your email/contact info]

---

## Acknowledgments

- OpenWeatherMap API (https://openweathermap.org/api)  
- PostgreSQL (https://www.postgresql.org)  
- Python data science libraries (Pandas, Scikit-learn, Matplotlib, Plotly)

---

Feel free to explore, reuse, and extend this project!
