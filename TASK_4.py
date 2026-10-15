import requests
import pandas as pd
from  CLIENT_INFO import client_id
import yaml

def heatwaves(scources = "SN17850", year = "2025") -> None:
    """Identifies and exports periods of heatwaves for a given weather station and year.

    Queries the MET Norway Frost API for daily maximum air temperatures, identifies
    consecutive periods of 5 or more days where temperatures reach or exceed 27°C,
    fetches the station's metadata name, and exports the summary to a YAML file.

    Args:
        scources: Frost station identifier (e.g., 'SN17850'). Defaults to 'SN17850'.
        year: Target year to query, formatted as a string or integer (e.g., '2025' or 2025).
            Defaults to '2025'.

    Returns:
        None. The results are printed to stdout and saved directly to a YAML file
        named 'Heatwaves_<scources>_<year>.yml'.

    Notes:
        Requires the global variable `client_id` to be defined for HTTP basic
        authentication with the Frost API.
    """
    #Inspired from "https://frost.met.no/python_example.html"
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': scources,
        'elements': 'max(air_temperature P1D)',
        'referencetime': f'{year}-01-01/{year}-12-31',
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
        return


    df = pd.json_normalize(
        data,
        record_path="observations",
        meta=["referenceTime", "sourceId"],
    )
    df["referenceTime"] = pd.to_datetime(df.referenceTime).dt.date
    df = df[df["timeOffset"]  == "PT0H"].reset_index(drop=True)
    
    #Had to collect station name from scources link rather than observations
    endpoint_sc = 'https://frost.met.no/sources/v0.jsonld'
    st_name = requests.get(
        endpoint_sc, params = {"ids":scources}, auth=(client_id,"")
    )
    st_name = st_name.json()["data"][0]["name"]
    
    deg27 = df["value"] >= 27 #Makes a boolean per day to check if  deg is more than 27

    run_id = (deg27 != deg27.shift()).cumsum() #Creates an per period id, new period each time it changes from more than 27 to less

    #Nicely formmats the data of the possible heatwaves
    runs = (df[deg27]
        .groupby(run_id)
        .agg(
                dates=("referenceTime", lambda s: f"{s.iloc[0]} - {s.iloc[-1]}"),
                consecutive_days = ('value', 'count'),
            ))
    print(runs)
    dates = (runs[runs["consecutive_days"] >= 5].reset_index(drop=True))
    date_list = (dates["dates"]).to_list()

    heatwave_summmary = {
        "dates": date_list,
        "station_id": scources,
        "station_name": st_name,
        "year": year
    }

    with open(f"Heatwaves_{scources}_{year}.yml", "w") as file:
        yaml.dump(heatwave_summmary, file, sort_keys=False)
    print("CODE FINISHED:  yaml file created")

heatwaves(year=2025)