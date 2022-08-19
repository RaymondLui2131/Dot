# Steps on using geocoding script:
1. Head to https://geoservice.planning.nyc.gov/ and create account to access mapquest geocoding api key
2. Download geocodingWithGeoSupport.py and a csv file containing addresses.
3. On line 7 in geoCoding.py change whatever your csv file name is to replace "accessible-pedestrian-signals.csv".
4. Replace line 11 to your mapquest api key.
5. Run geocodingWithGeoSupport.py and wait until a new shapefile is create. The new shapefile should have coordinates corresponding to the address given.


