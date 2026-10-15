import requests
import pandas as pd
from matplotlib import pyplot as plt
from TASK_1 import task_1
from  CLIENT_INFO import client_id

#Gotten from "https://frost.met.no/python_example.html"
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'sum(precipitation_amount P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}
# Issue an HTTP GET request
r = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
json = r.json()

if r.status_code == 200:
    data = json['data']
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])


df_p = pd.json_normalize(
    data,
    record_path="observations",
    meta=["referenceTime", "sourceId"],
)



df_p = df_p[df_p["timeOffset"] == "PT6H"].reset_index(drop=True)
df_p["referenceTime"] = pd.to_datetime(df_p["referenceTime"])




# 2. Setup dual-axis figure
fig, ax_temp = plt.subplots(figsize=(12, 6))
ax_precip = ax_temp.twinx()

# 3. Plot Temperature (Line) on ax_temp (Left Axis)
temp_dates, temp_values = task_1()
(line_temp,) = ax_temp.plot(
    temp_dates,
    temp_values,
    color="#d62728",  # Red line
    linewidth=1.8,
    label="Daily Mean Temperature",
)
ax_temp.set_ylabel("Daily Mean Temperature (°C)", color="#d62728", fontsize=11)
ax_temp.tick_params(axis="y", labelcolor="#d62728")
ax_temp.grid(True, linestyle="--", alpha=0.5)

# 4. Plot Precipitation (Bars) on ax_precip (Right Axis)
bar_precip = ax_precip.bar(
    df_p["referenceTime"],
    df_p["value"],
    width=0.8,
    color="#000055",  
    alpha=0.6,
    label="Precipitation (24h)",
)
unit_str = df_p["unit"][0]
ax_precip.set_ylabel(f"Precipitation ({unit_str})", color="#000055", fontsize=11)
ax_precip.tick_params(axis="y", labelcolor="#000055")
ax_precip.set_ylim(bottom=0)  # Precipitation cannot be negative

# 5. Bring line in front of the bars
ax_temp.set_zorder(ax_precip.get_zorder() + 1)
ax_temp.patch.set_visible(False)

# 6. Combined Legend
ax_temp.legend(
    [line_temp, bar_precip],
    ["Daily Mean Temperature", "Precipitation (24h)"],
    loc="upper left",
    framealpha=0.9,
)

# 7. Formatting
ax_temp.set_xlabel("Date", fontsize=11)
plt.title(
    "Daily Mean Temperature & 24h Precipitation – Ås (2025)",
    fontsize=13,
    weight="bold",
)

plt.tight_layout()
plt.show()