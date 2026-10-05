import requests
import pandas as pd


ids = open("CLIENT_INFO.txt","r")
client_id, client_secret = ids.readlines()
print(str(client_id))
#Gotten from "https://frost.met.no/python_example.html"
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'sum(precipitation_amount P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}
# Issue an HTTP GET request
r = requests.get(endpoint, parameters, auth=("5ceb0caf-ed69-47d8-8b8e-f668da8484e8",''))  #FJERN API KEY!!!
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
print(df.head())
