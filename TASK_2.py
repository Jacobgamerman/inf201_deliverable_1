import requests
import pandas as pd
from matplotlib import pyplot as plt
"""

ids = open("CLIENT_INFO.txt","r")
client_id, client_secret = ids.readlines()
print(str(client_id))
"""
from  CLIENT_INFO import client_id
#Gotten from "https://frost.met.no/python_example.html"
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'sum(precipitation_amount P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}
# Issue an HTTP GET request
r = requests.get(endpoint, parameters, auth=(client_id,''))  #FJERN API KEY!!!
# Extract JSON data
json = r.json()

if r.status_code == 200:
    data = json['data']
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])


df = pd.json_normalize(
    data,
    record_path="observations",
    meta=["referenceTime", "sourceId"],
)

df = df[df["timeOffset"]  == "PT6H"].reset_index(drop=True)
print(df.head())

plt.plot(df["value"])
plt.xlabel("Days")
plt.ylabel(f"Precipation ({df['unit'][0]})")
plt.show()