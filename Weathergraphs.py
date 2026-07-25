import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
def plot_weather_graph(csv_file, column, title, color,ylabel, figsize=(4, 3)):

    df = pd.read_csv(csv_file)

    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(
        df["date"],
        df[column],
        marker="o",
        markersize=3,
        linewidth=1.5,
        label=ylabel,
        color=color
    )

    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Date", fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)

    ax.tick_params(axis='both', labelsize=7)

    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.legend()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def rain_graph_last_30days(csv_file, column, title, ylabel, figsize=(4,3)):
    
    df = pd.read_csv(csv_file)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=figsize)

    ax.bar(df["date"], df[column] , label=ylabel)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
def weather_condition_pie_chart(csv_file, title, figsize=(4, 4)):

    WMO_WEATHER_CODES = {
        0: "Sunny",

        1: "Cloudy",
        2: "Cloudy",
        3: "Cloudy",

        45: "Fog",
        48: "Fog",

        51: "Drizzle",
        53: "Drizzle",
        55: "Drizzle",
        56: "Drizzle",
        57: "Drizzle",

        61: "Rainy",
        63: "Rainy",
        65: "Rainy",
        66: "Rainy",
        67: "Rainy",

        71: "Snowy",
        73: "Snowy",
        75: "Snowy",
        77: "Snowy",
        85: "Snowy",
        86: "Snowy",

        80: "Rain Showers",
        81: "Rain Showers",
        82: "Rain Showers",

        95: "Thunderstorm",
        96: "Thunderstorm",
        99: "Thunderstorm"
    }

    WEATHER_COLORS = {
        "Sunny": "#FFD700",
        "Cloudy": "#A9A9A9",
        "Fog": "#C0C0C0",
        "Drizzle": "#87CEEB",
        "Rainy": "#1E90FF",
        "Rain Showers": "#4169E1",
        "Snowy": "#FFFFFF",
        "Thunderstorm": "#800080",
        "Unknown": "#808080"
    }

    # Read CSV
    df = pd.read_csv(csv_file)

    # Check that weather_code exists
    if "weather_code" not in df.columns:
        st.error("The CSV does not contain a 'weather_code' column.")
        return

    # Create weather_condition column
    df["weather_condition"] = (
        df["weather_code"]
        .map(WMO_WEATHER_CODES)
        .fillna("Unknown")
    )

    # Count weather conditions
    counts = df["weather_condition"].value_counts()

    # Create matching color list
    colors = [
        WEATHER_COLORS.get(condition, "#808080")
        for condition in counts.index
    ]

    # Plot
    fig, ax = plt.subplots(figsize=figsize)

    wedges, texts, autotexts = ax.pie(
        counts,
        labels=None,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.legend(
        wedges,
        counts.index,
        title="Weather",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    ax.set_title(title)
    ax.axis("equal")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)