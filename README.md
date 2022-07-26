# Steps on using geocoding script:
1. Head to https://developer.mapquest.com/ and create account to access mapquest geocoding api key
2. Download geoCoding.py and a csv file containing addresses.
3. On line 5 in geoCoding.py change whatever your csv file name is to replace "accessible-pedestrian-signals.csv".
4. Replace line 11 to your mapquest api key.
5. Run geoCoding.py and wait until a new CSV file is create. The new CSV file should have coordinates corresponding to the address given.

PS. Script is not fully done as address with keyword "and" produces incorrect corrdinates.
