"""
TASK 5
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt

# Correct client ID
from CLIENT_INFO import client_id

# Frost API endpoint and parameters for daily mean air temperature
endpoint = "https://frost.met.no/observations/v0.jsonld"
parameters = {
    "sources": "SN17850",  # Weather station ID for Ås
    "elements": "mean(air_temperature P1D)",  # Daily mean air temperature
    "referencetime": "2025-01-01/2025-12-31",
}

# Send request to Frost API using client ID for authentication
response = requests.get(endpoint, params=parameters, auth=(client_id, ""))
data = response.json()

# Extract observations from the API response
obs = data["data"]

# Build a list of rows containing time and temperature values
rows = []
for item in obs:
    time = item["referenceTime"]          # Timestamp of the observation
    temp = item["observations"][0]["value"]  # Temperature value
    rows.append([time, temp])

# Create a DataFrame with time and temperature columns
df = pd.DataFrame(rows, columns=["time", "temperature"])

# Convert time column to datetime format
df["time"] = pd.to_datetime(df["time"])

# --- Task 5 requirement: function for 7-day moving average ---
def moving_average(series, window=7):
    """
    Calculate a moving average over a given window size.

    Args:
        series (pd.Series): Temperature values.
        window (int): Number of days for the moving average.

    Returns:
        pd.Series: Moving average values.
    """
    return series.rolling(window=window).mean()

# Calculate the 7-day moving average for 2025 temperatures
df["moving_avg"] = moving_average(df["temperature"], window=7)

# Plot daily temperature as points and moving average as a line
plt.figure(figsize=(12, 5))

# Daily temperature as scatter points
plt.scatter(df["time"], df["temperature"], color="royalblue", s=10, label="Daily Temperature")

# Moving average as line
plt.plot(df["time"], df["moving_avg"], color="darkred", linewidth=2, label="7-Day Moving Average")

plt.title("Daily Temperature and 7-Day Moving Average – Ås (2025)")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
