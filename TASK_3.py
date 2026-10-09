"""
TASK 3
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt

from CLIENT_INFO import client_id

# Frost API endpoint
endpoint = "https://frost.met.no/observations/v0.jsonld"

# Parameters for 2025 temperatures
parameters_2025 = {
    "sources": "SN17850",  # Weather station ID for Ås
    "elements": "mean(air_temperature P1D)",  # Daily mean air temperature
    "referencetime": "2025-01-01/2025-12-31",
}

# Parameters for 1925 temperatures
parameters_1925 = {
    "sources": "SN17850",  # Same station, 100 years earlier
    "elements": "mean(air_temperature P1D)",
    "referencetime": "1925-01-01/1925-12-31",
}

# Request 2025 data
response_2025 = requests.get(endpoint, params=parameters_2025, auth=(client_id, ""))
data_2025 = response_2025.json()
obs_2025 = data_2025["data"]

# Request 1925 data
response_1925 = requests.get(endpoint, params=parameters_1925, auth=(client_id, ""))
data_1925 = response_1925.json()
obs_1925 = data_1925["data"]

# Build DataFrame for 2025
rows_2025 = []
for item in obs_2025:
    time = item["referenceTime"]          # Timestamp of the observation
    temp = item["observations"][0]["value"]  # Temperature value
    rows_2025.append([time, temp])

df_2025 = pd.DataFrame(rows_2025, columns=["time", "temperature"])
df_2025["time"] = pd.to_datetime(df_2025["time"])

# Build DataFrame for 1925
rows_1925 = []
for item in obs_1925:
    time = item["referenceTime"]
    temp = item["observations"][0]["value"]
    rows_1925.append([time, temp])

df_1925 = pd.DataFrame(rows_1925, columns=["time", "temperature"])
df_1925["time"] = pd.to_datetime(df_1925["time"])

# Normalize dates to day-of-year so the curves can be compared properly
df_2025["dayofyear"] = df_2025["time"].dt.dayofyear
df_1925["dayofyear"] = df_1925["time"].dt.dayofyear

# Plot both temperature curves in the same figure
plt.figure(figsize=(12, 5))
plt.plot(df_2025["dayofyear"], df_2025["temperature"], color="royalblue", label="2025")
plt.plot(df_1925["dayofyear"], df_1925["temperature"], color="darkred", label="1925")

plt.title("Daily Mean Temperature – Ås (2025 vs 1925)")
plt.xlabel("Day of Year")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Create summary table for both years
summary = {
    "Mean_2025": df_2025["temperature"].mean(),
    "Median_2025": df_2025["temperature"].median(),
    "Min_2025": df_2025["temperature"].min(),
    "Max_2025": df_2025["temperature"].max(),

    "Mean_1925": df_1925["temperature"].mean(),
    "Median_1925": df_1925["temperature"].median(),
    "Min_1925": df_1925["temperature"].min(),
    "Max_1925": df_1925["temperature"].max()
}

summary_df = pd.DataFrame([summary])
print(summary_df)
