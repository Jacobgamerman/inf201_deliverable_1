"""
TASK 1
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt

from CLIENT_INFO import client_id

# Frost API endpoint and parameters for daily mean air temperature
endpoint = "https://frost.met.no/observations/v0.jsonld"
parameters = {
    "sources": "SN17850",  # Weather station ID for Ås
    "elements": "mean(air_temperature P1D)",  # Daily mean air temperature
    "referencetime": "2025-01-01/2025-12-31",  # Full year of 2025
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

# Plot daily mean temperature throughout the year
plt.figure(figsize=(12,5))
plt.plot(df["time"], df["temperature"], color="royalblue")

plt.title("Daily Mean Temperature – Ås (2025)")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.tight_layout()
plt.show()

# Create a summary table with basic statistics
summary = {
    "Mean": df["temperature"].mean(),
    "Median": df["temperature"].median(),
    "Min": df["temperature"].min(),
    "Max": df["temperature"].max()
}

summary_df = pd.DataFrame([summary])
print(summary_df)
