import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from streamlit_geolocation import streamlit_geolocation
import weatherreport
import hourly_weatherreport
import Weathergraphs
import time 
import AI

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Weather App",
    page_icon="🌦️",
    layout="wide"
)


# ==========================================================
# API KEY
# ==========================================================

API_KEY = st.secrets["api_key"]


# ==========================================================
# LOAD PROMPT FILES
# ==========================================================

with open("System_prompt.txt", "r", encoding="utf-8") as system_file:
    system_prompt_text = system_file.read()

st.session_state.setdefault("ai_model", AI.DEFAULT_MODEL)
st.session_state.setdefault("ai_temperature", AI.DEFAULT_TEMPERATURE)
st.session_state.setdefault("ai_system_prompt", system_prompt_text)

with open("User_prompt.txt", "r", encoding="utf-8") as user_file:
    user_prompt_text = user_file.read()

with open("Prediction_prompt.txt" , "r" , encoding="utf-8") as prediction_file:
    prediction_prompt_text = prediction_file.read()

# ==========================================================
# LOCATION DETECTION
# ==========================================================
# Try to get the user's current location using browser GPS.
# If the user denies access, we will show a manual city input.
# ==========================================================
st.markdown(
    """
    <div style="
        background: #111827;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 3px solid #38BDF8;
        margin-bottom: 14px;
    ">
        <div style="
            color: #E5E7EB;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.2px;
        ">
            📍 Get weather for your current location
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

location = streamlit_geolocation()

url = None
city = None


# ==========================================================
# MANUAL LOCATION INPUT
# ==========================================================

st.markdown(
    """
    <div style="
        background: #111827;
        padding: 12px 16px;
        border-radius: 10px;
        border-left: 3px solid #38BDF8;
        margin-bottom: 14px;
    ">
        <div style="
            color: #E5E7EB;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 0.2px;
        ">
            🔎 Search weather by location
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

city = st.text_input(
    "Enter the location",
    placeholder="e.g. Kolkata",
    key="city_search_input",
    autocomplete="country"
).strip()

# ==========================================================
# USE MANUAL LOCATION IF PROVIDED
# ==========================================================

if city:

    st.info(f"Showing the availabe reports for : {city}")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

# ==========================================================
# OTHERWISE USE GPS LOCATION
# ==========================================================

elif (
    location
    and location.get("latitude") is not None
    and location.get("longitude") is not None
):

    lat = location["latitude"]
    lon = location["longitude"]

    st.success("📍 Location detected automatically")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}"
        f"&lon={lon}"
        f"&appid={API_KEY}"
        f"&units=metric"
    )

# ==========================================================
# NO LOCATION AVAILABLE
# ==========================================================

else:

    st.warning(
        "Location permission denied or unavailable.\n"
        "Please enter a location manually."
    )
    st.stop()


# ==========================================================
# WEATHER DATA FETCHING
# ==========================================================

data = None

try:

    with st.spinner("Fetching weather data..."):

        response = requests.get(url, timeout=10)

    if response.status_code == 200:

        data = response.json()

        # Actual city name returned by API
        city = data["name"]

    else:

        st.error("❌ Unable to find this location.")
        st.stop()

except requests.exceptions.RequestException:

    st.error("⚠️ Unable to connect to OpenWeatherMap.")
    st.stop()


# ==========================================================
# CACHE WEATHER REPORT GENERATION
# ==========================================================
# Prevents generating the same CSV every time the app reruns.
# ==========================================================


def generate_historical_report(lat, lon):
    try:
        weatherreport.generate_30_day_report(lat, lon)
        weatherreport.generate_30_day_daily_all_report(lat,lon)
        hourly_weatherreport.generate_hourly_weather_report(lat, lon)
        hourly_weatherreport.generate_all_hourly_weather_report(lat, lon)
    except Exception as exc:
        st.warning(f"Historical weather data could not be generated: {exc}")


# ==========================================================
# GRAPH FUNCTION
# ==========================================================
tab1, tab2, tab3 = st.tabs([
    "Weather Insights",
    "Weather Data Visualization",
    "For Developers"
])


# ==========================================================
# TAB 1 : CURRENT WEATHER
# ==========================================================

with tab1:

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "🌡 Temperature",
        f"{data['main']['temp']} °C"
    )

    col2.metric(
        "💧 Humidity",
        f"{data['main']['humidity']} %"
    )

    col3.metric(
        "🥵 Feels Like",
        f"{data['main']['feels_like']} °C"
    )

    col4.metric(
        "💨 Wind Speed",
        f"{data['wind']['speed']} m/s"
    )

    col5.metric(
        "🌤 Weather",
        data["weather"][0]["description"].title()
    )

    # ------------------------------------------------------
    # LIVE CLOCK
    # ------------------------------------------------------

    timezone_offset = data["timezone"]

    @st.fragment(run_every="1s")
    def live_clock():

        utc_now = datetime.now(timezone.utc)

        local_time = utc_now + timedelta(
            seconds=timezone_offset
        )

        st.metric(
            f"🕒 Current Time in {city}",
            local_time.strftime("%H:%M:%S")
        )

    live_clock()

    # ------------------------------------------------------
    # LOCATION INFORMATION
    # ------------------------------------------------------

    latitude = data["coord"]["lat"]
    longitude = data["coord"]["lon"]

    st.write(f"📍 Latitude: {latitude}")
    st.write(f"📍 Longitude: {longitude}")

    # ------------------------------------------------------
        # HISTORICAL WEATHER DATA
        # ------------------------------------------------------
            
    with st.spinner("Generating historical weather report..."):

        generate_historical_report(
            latitude,
            longitude
        )
        

    try:

        df = pd.read_csv(
            "weather_last_30_days.csv"
        )

        # st.subheader(
        #     f"📊 Historical Weather Data of {city}"
        # )

        # st.dataframe(
        #     df,
        #     use_container_width=True
        # )

    except FileNotFoundError:

        st.warning(
            "Historical weather data could not be generated."
        )

    try:
        df_hourly = pd.read_csv("hourly_weather.csv")
        # st.subheader(
        #     f"📊Hourly Historical Weather Data of {city}"
        # )
        
        # st.dataframe(
        #     df_hourly,
        #     use_container_width=True
        # )
    except FileNotFoundError:
        st.warning(
            "Historical weather data could not be generated."
        )
        

    # ------------------------------------------------------
    # AI Response 
    # ------------------------------------------------------
    st.divider()
    

    st.markdown("""
    <style>
    div.stButton > button {
        background-color: #38BDF8;
        color: white;
        border: none;
        border-radius: 8px;
    }

    div.stButton > button:hover {
        background-color: #0f47ae;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("Tap here to genrate the Weather prediction according to AI 🤖", type="primary"):
        with st.spinner("Generating Weather predictions with AI", show_time=True):
            st.title("🌦️ Weather AI Analyst")

            df = pd.read_csv("weather_daily_all_report.csv")

            st.subheader("Weather Data")
            # st.dataframe(df)
            system_prompt = st.session_state["ai_system_prompt"]

            prediction_prompt_input = f"""Use {df.to_string()} , and {prediction_prompt_text}"""

            st.subheader("🤖 Weather Prediction according to AI")

            full_text = ""
            placeholder = st.empty()

            for chunk in AI.AI_Response(
                prediction_prompt_input,
                system_prompt,
                model=st.session_state["ai_model"],
                temperature=st.session_state["ai_temperature"],
            ):
                if chunk["type"] == "content":
                    full_text += chunk["content"]
                    placeholder.markdown(full_text, unsafe_allow_html=True)

    st.divider()

    if st.button("Tap here to generate AI weather analysis 🤖"):
        with st.spinner("Generating Weather analytics with AI", show_time=True):
            st.title("🌦️ Weather AI Analyst")

            df = pd.read_csv("weather_daily_all_report.csv")

            st.subheader("Weather Data")
            # st.dataframe(df)
            system_prompt = st.session_state["ai_system_prompt"]

            prompt = f"""Use {df.to_string()} , and {user_prompt_text}"""

            st.subheader("🤖 AI Analysis")

            full_text = ""
            placeholder = st.empty()

            for chunk in AI.AI_Response(
                prompt,
                system_prompt,
                model=st.session_state["ai_model"],
                temperature=st.session_state["ai_temperature"],
            ):
                if chunk["type"] == "content":
                    full_text += chunk["content"]
                    placeholder.markdown(full_text, unsafe_allow_html=True)
    

# ==========================================================
# TAB 2 : VISUALIZATIONS
# ==========================================================


    
with tab2:

    def section_header(icon, title, color="#1E88E5"):
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {color}, #64B5F6);
            padding:10px;
            border-radius:10px;
            margin-top:8px;
            margin-bottom:8px;
            box-shadow:0 3px 10px rgba(0,0,0,0.15);
        ">
            <h4 style="
                color:white;
                margin:0;
                text-align:center;
                font-size:16px;
            ">
                {icon} {title}
            </h4>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
                <style>
                .graph-card {
                    background-color: #ffffff;
                    padding: 8px;
                    border-radius: 12px;
                    border: 1px solid #ddd;
                    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
                    margin: 0;
                    height: 100%;
                }
                /* Streamlit columns render as flex containers by default,
                   this just tightens the gap and aligns items */
                div[data-testid="stHorizontalBlock"] {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    align-items: stretch;
                }
                div[data-testid="column"] {
                    flex: 1 1 300px;
                }
                </style>
                """, unsafe_allow_html=True)
    
    
    with st.spinner("Generating dashboard...", show_time=True):
        time.sleep(4)
        col1, col2, col3 , col4 = st.columns(4)

        with col1:
            
            section_header("📈", f"Max Temp – {city}")
            Weathergraphs.plot_weather_graph(
                "weather_last_30_days.csv",
                "temp_max",
                "Maximum Temperature (30 Days)",
                "orange",
                "Temperature (°C)",
                figsize=(4, 3)
            )

        with col2:
            section_header("📉", f"Min Temp – {city}")
            Weathergraphs.plot_weather_graph(
                "weather_last_30_days.csv",
                "temp_min",
                "Minimum Temperature (30 Days)",
                "cyan",
                "Temperature (°C)",
                figsize=(4, 3)
            )

        with col3:
            section_header("🌧", f"Rainfall – {city}")
            Weathergraphs.rain_graph_last_30days(
                "weather_last_30_days.csv",
                "rain_mm",
                "Rainfall (30 Days)",
                "Rainfall (mm)",
                figsize=(4, 3)
            )
        
        with col4:
            section_header("🌧", f"Weather condition – {city}")
            Weathergraphs.weather_condition_pie_chart(
                            "weather_daily_all_report.csv",
                            "Weather Condition (30 Days)"
            )

# ==========================================================
# TAB 3 : For Developers
# ==========================================================

with tab3:
    st.markdown(
        """
        <div class="developer-hero">
            <div class="developer-eyebrow">WEATHER AI · DEVELOPER TOOLS</div>
            <h2>Configure your AI experience</h2>
            <p>Adjust the model and instructions used for weather predictions and analysis.</p>
        </div>
        <style>
        .developer-hero {
            padding: 1.5rem 1.75rem;
            margin: 0 0 1.25rem;
            border: 1px solid rgba(56, 189, 248, 0.32);
            border-radius: 16px;
            background: linear-gradient(125deg, rgba(14, 116, 144, 0.24), rgba(30, 41, 59, 0.78));
        }
        .developer-hero h2 {
            margin: 0.25rem 0 0.4rem;
            color: #f8fafc;
        }
        .developer-hero p {
            margin: 0;
            color: #cbd5e1;
        }
        .developer-eyebrow {
            color: #7dd3fc;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.14em;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.subheader("AI settings")
        st.caption("These settings apply to both weather predictions and AI analysis.")
        model_col, temperature_col = st.columns([2, 1])

        with model_col:
            st.text_input(
                "NVIDIA model",
                key="ai_model",
                help="Enter a model name from NVIDIA's inference catalog.",
            )

        with temperature_col:
            st.slider(
                "Model temperature",
                min_value=0.0,
                max_value=2.0,
                step=0.05,
                key="ai_temperature",
                help="Lower values are more focused; higher values are more varied.",
            )

        st.text_area(
            "System prompt",
            key="ai_system_prompt",
            height=220,
            help="Instructions that guide both AI weather features.",
        )

        st.link_button(
            "View GitHub repository",
            "https://github.com/shirshadip/AiWeatherApp",
        )

    st.subheader("Weather API response")
    st.caption("Raw OpenWeatherMap response for the selected location.")
    with st.container(border=True):
        st.json(data, expanded=False)
    


  
st.divider()
st.write("© 2026 , All rights reserved -- shirshadip ")