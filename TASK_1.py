import requests
import pandas as pd
import matplotlib.pyplot as plt

# Sett inn din egen client-id her
from CLIENT_INFO import client_id

endpoint = "https://frost.met.no/observations/v0.jsonld"
parameters = {
    "sources": "SN17850",
    "elements": "mean(air_temperature P1D)",
    "referencetime": "2025-01-01/2025-12-31",
}

# Send forespørsel
response = requests.get(endpoint, params=parameters, auth=(client_id, ""))
data = response.json()

# Plukk ut observasjoner
obs = data["data"]

# Lag DataFrame
rows = []
for item in obs:
    time = item["referenceTime"]
    temp = item["observations"][0]["value"]
    rows.append([time, temp])

df = pd.DataFrame(rows, columns=["time", "temperature"])

# Konverter tid til datetime
df["time"] = pd.to_datetime(df["time"])

# Plot temperatur gjennom året
plt.figure(figsize=(12,5))
plt.plot(df["time"], df["temperature"], color="royalblue")

plt.title("Daglig middeltemperatur – Ås (2025)")
plt.xlabel("Dato")
plt.ylabel("Temperatur (°C)")
plt.grid(True)

plt.tight_layout()
plt.show()

# Oppsummeringstabell
summary = {
    "Mean": df["temperature"].mean(),
    "Median": df["temperature"].median(),
    "Min": df["temperature"].min(),
    "Max": df["temperature"].max()
}

summary_df = pd.DataFrame([summary])
print(summary_df)
