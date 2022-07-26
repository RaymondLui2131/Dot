import pandas as pd
import requests
import json

dataFrame = pd.read_csv("accessible-pedestrian-signals.csv")

for i, row in dataFrame.iterrows():
    addressesNY = str(dataFrame.at[i, 'Location']) + ',' + str(dataFrame.at[i, 'Borough'])

    parameters = {
        "key": "X6obCOYUiA4QXG4z8OARsOcDLjer7KGe",
        "location": addressesNY
    }

    response = requests.get("https://www.mapquestapi.com/geocoding/v1/address", params=parameters)

    data = json.loads(response.text)['results']
    lat = (data[0]['locations'][0]['latLng']['lat'])
    lng = (data[0]['locations'][0]['latLng']['lng'])

    dataFrame.at[i, 'lat'] = lat
    dataFrame.at[i, 'lng'] = lng

dataFrame.to_csv('finalCheckCoords.csv')
