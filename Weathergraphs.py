import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
def plot_weather_graph(csv_file, column, title, ylabel, figsize=(4, 3)):

    df = pd.read_csv(csv_file)

    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(
        df["date"],
        df[column],
        marker="o",
        markersize=3,
        linewidth=1.5,
        label=ylabel
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