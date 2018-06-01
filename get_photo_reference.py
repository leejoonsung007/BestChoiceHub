import pandas as pd
import googlemaps
import os
from collections import defaultdict

KEY = "AIzaSyDL_YVLa4qg-Pi4Q_W_10e1Kiih_b8Hmv0"
gmaps = googlemaps.Client(key=KEY)

data = pd.read_csv('post_primary_school_list.csv')
data = data[0:713]
data = data.fillna('')
school_addresses = data['Official School Name'] + ' ' + data['Address 1'] + ' ' + data['Address 2'] + ' ' + data['Address 3'] + ' ' + data['Address 4']

#get the place_id for next step
placeid = []
for school_address in school_addresses:
    address = school_address
    result = gmaps.geocode(address)
    for r in result:
        placeid.append (r['place_id'])

# use place_id to get the details of the place and get the photo reference
name_photoref = defaultdict(list)
values_list = []
for id in placeid:
    response = gmaps.place(place_id=id)
    name = (response['result'])['name']
    print(name)
    try:
        photos = (response['result'])['photos']
        for photo in photos:
            name_photoref[name].append(photo['photo_reference'])
    except:
        pass
    values = name_photoref[name]
    values_list.append(values)

reference = pd.DataFrame(values_list)
data[reference.columns] = reference
data.to_csv('new.csv')
print("the file have been saved" + os.getcwd())
