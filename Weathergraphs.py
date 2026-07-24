import pandas as pd
import matplotlib.pyplot as plt

def plot_weather_graph(csv_file, column, title, ylabel):
    """
    Plots a weather graph from a CSV file.

    Parameters:
        csv_file (str): Path to the CSV file.
        column (str): Column name to plot.
        title (str): Graph title.
        ylabel (str): Y-axis label.
    """

    # Read CSV
    df = pd.read_csv(csv_file)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Create graph
    plt.figure(figsize=(12, 5))
    plt.plot(df["date"], df[column], marker="o")

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()
    plt.show()
    
    
def rain_graph_last_30days(csv_file, column, title, ylabel, figsize=(4,3)):
    
    df = pd.read_csv(csv_file)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    fig, ax = plt.subplots(figsize=figsize)

    ax.bar(df["date"], df[column])
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig

    