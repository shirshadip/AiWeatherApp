# 🌦️ WeatherApp - Setup & Run Guide

## ✅ App Status: READY TO RUN

All issues have been fixed! Here's what was corrected:

### Fixed Issues:

✓ **Circular Import Removed** - `weatherreport.py` no longer imports `app`
✓ **Secrets Handling Fixed** - API key is now safely accessed with error handling
✓ **Docker Removed** - Focus on local development first
✓ **Dependencies Updated** - `requests` added to requirements.txt
✓ **Streamlit Configured** - Proper configuration in `.streamlit/config.toml`

---

## 🚀 Running the App Locally

### Prerequisites:

- Python 3.8+
- Virtual environment activated (`.venv`)
- All dependencies installed

### Run the App:

```bash
# Option 1: Simple run
streamlit run app.py

# Option 2: With custom port
streamlit run app.py --server.port 8501

# Option 3: With logging
streamlit run app.py --logger.level=debug
```

The app will open at: **http://localhost:8501**

---

## 📋 What the App Does:

1. **Automatic Location Detection** - Uses browser GPS if permitted
2. **Manual Location Input** - Enter city name as fallback
3. **Current Weather Tab** - Displays real-time weather metrics
   - Temperature, Humidity, Feels Like
   - Wind Speed, Weather Condition
   - Live clock for the city's timezone
   - Latitude & Longitude

4. **Weather Visualizations Tab** - 30-day historical data graphs
   - Maximum Temperature Chart
   - Minimum Temperature Chart
   - Rainfall Chart

5. **Raw JSON Tab** - Display raw API response

---

## 📁 Project Structure:

```
WeatherApp/
├── app.py                      # Main Streamlit app
├── weatherreport.py            # Generate 30-day weather reports
├── weather_data.py             # Weather data utilities
├── getloc.py                   # Geolocation utilities
├── requirements.txt            # Python dependencies
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml           # API keys (gitignored)
├── weather_last_30_days.csv   # Generated historical data
└── README.md                   # Original project README
```

---

## 🔑 API Configuration:

Your OpenWeatherMap API key is stored in:

```
.streamlit/secrets.toml
```

Add both API keys to that file so the app can fetch weather and generate AI analysis:

```toml
api_key = "your_openweathermap_api_key_here"
AI_API_KEY = "your_nvidia_api_key_here"
```

The AI analysis uses NVIDIA's OpenAI-compatible API with the `nvidia/nemotron-3-ultra-550b-a55b` model. Keep the keys private; `secrets.toml` is gitignored.

To change either key:

1. Edit `.streamlit/secrets.toml`
2. Replace the corresponding key value
3. Restart the app

---

## ⚠️ Troubleshooting:

### App won't start?

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Streamlit cache
streamlit cache clear
```

### Location not detected?

- Allow browser geolocation access when prompted
- Use manual city input as fallback

### API errors?

- Check internet connection
- Verify API key in `.streamlit/secrets.toml`
- Check OpenWeatherMap API status

---

## 🐳 Docker Setup (Future)

When ready to containerize:

1. Create `Dockerfile` with proper base image
2. Create `docker-compose.yml` with volume mounts
3. Use `.env` for environment variables

For now, stick with local development!

---

**Happy weather checking! 🌤️**
