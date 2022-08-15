import pandas as pd
import requests
import json
import geopandas as gpd


df = pd.read_csv("accessible-pedestrian-signals.csv")

# api key and links
apiKey = "tXetIVc1RNhRj1Us"
Function2 = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_2?"
Function3 = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_3?"

# Looping addresses
for i, row in df.iterrows():
    address = str(df.at[i, 'Location'])
    Borough = str(df.at[i, 'Borough'])
    # Function 2 for "and" or "at"
    street1OA = str(df.at[i, 'Location']).rpartition('and')[0]
    street2OA = str(df.at[i, 'Location']).rpartition('and')[2]
    street1At = str(df.at[i, 'Location']).rpartition('at')[0]
    street2At = str(df.at[i, 'Location']).rpartition('at')[2]
    # Function 3 for "between, "and"
    onStrB = str(df.at[i, 'Location']).rpartition(' between ')[0]
    secCrsStrB = str(df.at[i, 'Location'])[
                 str(df.at[i, 'Location']).find(" between ") + len(" between "):str(df.at[i, 'Location']).rfind(
                     " and ")]
    frtCrStrB = str(df.at[i, 'Location']).rpartition(' and ')[2]
    # Function 3 for "with", "and"
    onStrW = str(df.at[i, 'Location']).rpartition(' with ')[0]
    secCrsStrW = str(df.at[i, 'Location'])[
                 str(df.at[i, 'Location']).find(" with ") + len(" with "):str(df.at[i, 'Location']).rfind(" and ")]
    frtCrStrW = str(df.at[i, 'Location']).rpartition(' and ')[2]

    # if for addresses with only and
    if not ("between" in str(df.at[i, 'Location']) or "with" in str(df.at[i, 'Location']) or "at" in str(
            df.at[i, 'Location'])):
        try:
            parameters = {
                "Borough1": Borough,
                "Street1": street1OA,
                "Borough2": Borough,
                "Street2": street2OA,
                "Borough3": Borough,
                "Key": apiKey,
            }

            response = requests.get(Function2, params=parameters)
            data = json.loads(response.text)['display']
            jsonData = pd.json_normalize(data)
            lat = float(data['out_latitude'])
            lng = float(data['out_longitude'])

            df.at[i, 'lat'] = lat
            df.at[i, 'lng'] = lng
        except:
            print('Not geocoded: ' + str(df.at[i, 'Location']))

    # if for addresses with only at
    elif not ("between" in str(df.at[i, 'Location']) or "with" in str(df.at[i, 'Location']) or "and" in str(
            df.at[i, 'Location'])):
        try:
            parameters = {
                "Borough1": Borough,
                "Street1": street1At,
                "Borough2": Borough,
                "Street2": street2At,
                "Borough3": Borough,
                "Key": apiKey,
            }

            response = requests.get(Function2, params=parameters)

            data = json.loads(response.text)['display']
            jsonData = pd.json_normalize(data)
            lat = float(data['out_latitude'])
            lng = float(data['out_longitude'])

            df.at[i, 'lat'] = lat
            df.at[i, 'lng'] = lng
        except:
            print('Not geocoded: ' + str(df.at[i, 'Location']))

    # if for addresses with "between" and "and"
    elif "between" in str(df.at[i, 'Location']) and "and" in str(df.at[i, 'Location']):
        try:
            parameters = {
                "Borough1": Borough,
                "OnStreet": onStrB,
                "SecondCrossStreet": secCrsStrB,
                "Borough2": Borough,
                "FirstCrossStreet": frtCrStrB,
                "Borough3": Borough,
                "Key": apiKey,
            }

            response = requests.get(Function3, params=parameters)

            data = json.loads(response.text)['display']
            jsonData = pd.json_normalize(data)
            out_from_lat = float(data['out_from_latitude'])
            out_from_lng = float(data['out_from_longitude'])
            out_to_lat = float(data['out_to_latitude'])
            out_to_lng = float(data['out_to_longitude'])

            df.at[i, 'lat'] = out_from_lat
            df.at[i, 'lng'] = out_from_lng
            df.at[i, 'lat2'] = out_to_lat
            df.at[i, 'lng2'] = out_to_lng
        except:
            print('Not geocoded: ' + str(df.at[i, 'Location']))

    # if for address with "with" and "and"
    elif "with" in str(df.at[i, 'Location']) and "and" in str(df.at[i, 'Location']):
        try:
            parameters = {
                "Borough1": Borough,
                "OnStreet": onStrW,
                "SecondCrossStreet": secCrsStrW,
                "Borough2": Borough,
                "FirstCrossStreet": frtCrStrW,
                "Borough3": Borough,
                "Key": apiKey,
            }

            response = requests.get(Function3, params=parameters)

            data = json.loads(response.text)['display']
            jsonData = pd.json_normalize(data)
            out_from_lat = float(data['out_from_latitude'])
            out_from_lng = float(data['out_from_longitude'])
            out_to_lat = float(data['out_to_latitude'])
            out_to_lng = float(data['out_to_longitude'])

            df.at[i, 'lat'] = out_from_lat
            df.at[i, 'lng'] = out_from_lng
            df.at[i, 'lat2'] = out_to_lat
            df.at[i, 'lng2'] = out_to_lng
        except:
            print('Not geocoded: ' + str(df.at[i, 'Location']))


# save coordinates into another csv file
file = df.to_csv('accessible-signals-geocoded.csv')

# save coordinates into a shp file
coords_data = pd.read_csv('accessible-signals-geocoded.csv')
coords_gdf = gpd.GeoDataFrame(coords_data, geometry=gpd.points_from_xy(coords_data['lat'], coords_data['lng']))
coords_gdf.to_file("geoSupportTest-InShapeFile1.shp")

coords_gdf2 = gpd.GeoDataFrame(coords_data, geometry=gpd.points_from_xy(coords_data['lat2'], coords_data['lng2']))
coords_gdf2.to_file("geoSupportTest-InShapeFile2.shp")

gdf1 = gpd.read_file('geoSupportTest-InShapeFile1.shp')
gdf2 = gpd.read_file('geoSupportTest-InShapeFile2.shp')

gdf = gpd.pd.concat([gdf1, gdf2])
gdf.to_file("finalShapeFile.shp")
