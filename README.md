# AI Weather App 🌦️

A professional, feature-rich weather application built with **Streamlit** that provides real-time weather data, 30-day forecasts, and interactive data visualizations.

## Overview

The AI Weather App delivers comprehensive weather insights for any location worldwide. It leverages the **OpenWeatherMap API** and **Open-Meteo Archive API** to fetch current conditions and historical weather data, presenting information through an intuitive web interface with advanced analytics.

## Features

✨ **Current Weather Metrics**

- Real-time temperature, humidity, and wind speed
- "Feels like" temperature index
- Live weather conditions with descriptions
- Dynamic local time display for searched locations
- Precise latitude/longitude coordinates

📈 **Historical Analysis (30-Day Reports)**

- Maximum and minimum temperature trends
- Rainfall data visualization
- Daily weather metrics archived automatically
- Interactive graphs with date range navigation

📊 **Data Visualization**

- Matplotlib-powered interactive charts
- Temperature trend analysis
- Precipitation patterns
- Responsive, mobile-friendly layouts

⚡ **Live Updates**

- Real-time clock synchronized to location timezone
- Auto-refreshing weather metrics
- Seamless API integration with error handling

## Tech Stack

| Component           | Technology                 |
| ------------------- | -------------------------- |
| **Frontend**        | Streamlit                  |
| **Data Processing** | Pandas, NumPy              |
| **Visualization**   | Matplotlib, Scikit-learn   |
| **Weather APIs**    | OpenWeatherMap, Open-Meteo |
| **Language**        | Python 3.x                 |
| **Analysis**        | Jupyter Notebooks, SciPy   |

## Project Structure

```
WeatherApp/
├── app.py                        # Main Streamlit application
├── weatherreport.py              # 30-day weather report generator
├── hourly_weatherreport.py       # Hourly weather data fetcher
├── weather_data.py               # Weather data utilities
├── Weathergraphs.py              # Graph plotting functions
├── model.ipynb                   # ML model development notebook
├── graphs.ipynb                  # Data visualization notebook
├── requirements.txt              # Python dependencies
├── test.py                       # Unit tests
├── hourly_weather.csv            # Hourly weather cache
├── weather_last_30_days.csv      # 30-day historical data
└── .streamlit/                   # Streamlit configuration
```

## Prerequisites

- **Python 3.8+**
- **pip** or conda package manager
- **OpenWeatherMap API Key** ([Get one free](https://openweathermap.org/api))

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/WeatherApp.git
cd WeatherApp
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create or update `.streamlit/secrets.toml`:

```toml
api_key = "your_openweathermap_api_key_here"
AI_API_KEY = "your_nvidia_api_key_here"
```

Get a weather API key from [OpenWeatherMap](https://openweathermap.org/api) and an inference API key from NVIDIA. Keep both keys private; do not commit `secrets.toml`.

## Usage

### Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Generate Weather Reports

Generate 30-day reports for specific coordinates:

```bash
# For Kolkata (default)
python weatherreport.py

# For custom location
python weatherreport.py --lat 40.7128 --lon -74.0060  # New York
```

### Fetch Hourly Weather Data

```bash
python hourly_weatherreport.py
```

## API Configuration

### Environment Variables

Set the API key as an environment variable (alternative to secrets.toml):

```bash
# Windows
set OPENWEATHER_API_KEY=your_api_key

# macOS/Linux
export OPENWEATHER_API_KEY=your_api_key
```

## Dependencies

| Package        | Version | Purpose              |
| -------------- | ------- | -------------------- |
| `streamlit`    | Latest  | Web framework        |
| `pandas`       | Latest  | Data manipulation    |
| `numpy`        | Latest  | Numerical computing  |
| `matplotlib`   | Latest  | Data visualization   |
| `requests`     | Latest  | HTTP requests        |
| `scikit-learn` | Latest  | ML utilities         |
| `scipy`        | Latest  | Scientific computing |

See `requirements.txt` for complete list.

## Features Breakdown

### Tab 1: Current Weather

- Displays real-time metrics in an intuitive card layout
- Shows location coordinates
- Automatically generates 30-day historical report
- Displays historical weather data table

### Tab 2: Weather Data Visualization

- Interactive graphs of temperature trends
- Rainfall patterns over 30 days
- Matplotlib-powered visualizations
- Responsive design for all screen sizes

### Tab 3: For Developers

- Configure the NVIDIA model, generation temperature, and system prompt
- Open the [AiWeatherApp GitHub repository](https://github.com/shirshadip/AiWeatherApp)
- Inspect the raw weather API response as JSON

## Testing

Run the test suite:

```bash
python test.py
```

## Error Handling

The application includes robust error handling:

- **City Not Found**: Returns user-friendly error message
- **Connection Failures**: Graceful timeout handling
- **Missing API Key**: Clear instructions for configuration
- **Data Processing Errors**: Fallback mechanisms

## Performance Optimization

- Caching of weather data in CSV format
- Efficient DataFrame operations with Pandas
- Optimized graph rendering with Matplotlib
- Smart API request management

## Browser Support

- Chrome/Chromium (Recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

### Running in Development Mode

```bash
streamlit run app.py --logger.level=debug
```

### Code Quality Tools

```bash
# Lint check
pylint *.py

# Format code
black *.py
```

## Jupyter Notebooks

The project includes interactive notebooks for analysis:

- **model.ipynb**: Machine learning model development
- **graphs.ipynb**: Data visualization experiments

Open with:

```bash
jupyter notebook model.ipynb
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Write/update tests
5. Submit a pull request

## Troubleshooting

| Issue                | Solution                                      |
| -------------------- | --------------------------------------------- |
| API Key not found    | Check `.streamlit/secrets.toml` file exists   |
| City not found error | Verify city name spelling                     |
| Connection timeout   | Check internet connection, API service status |
| CSV file not found   | Run `weatherreport.py` to generate data       |
| Import errors        | Run `pip install -r requirements.txt` again   |

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## Author

**Shirshadip** - [GitHub Profile](https://github.com/yourusername)

## Acknowledgments

- 🙏 [OpenWeatherMap](https://openweathermap.org/) for weather API
- 🙏 [Open-Meteo](https://open-meteo.com/) for historical weather data
- 🙏 [Streamlit](https://streamlit.io/) for the web framework
- 🙏 Community contributors

## Support & Contact

For issues, questions, or suggestions:

- 📧 Email: [mailto:shirshadiphere@gmail.com]
- 🐛 [Report a Bug](https://github.com/shirshadip/WeatherApp/issues)
- 💡 [Request a Feature](https://github.com/shirshadip/WeatherApp/issues)

---

**⭐ If you find this project helpful, please consider giving it a star!**

Last Updated: June 2026
