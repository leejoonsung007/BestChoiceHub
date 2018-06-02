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
coordinate = []
for school_address in school_addresses:
    address = school_address
    result = gmaps.geocode(address)
    for r in result:
        placeid.append (r['place_id'])
        coordinate.append((r['geometry'])['location'])

# use place_id to get the details of the place and get the photo reference
name_photoref = defaultdict(list)
values_list = []
for id in placeid:
    response = gmaps.place(place_id=id)
    name = (response['result'])['name']
    try:
        photos = (response['result'])['photos']
        for photo in photos:
            name_photoref[name].append(photo['photo_reference'])
    except:
        pass
    values = name_photoref[name]
    values_list.append(values)

# convert data to DataFrame
reference = pd.DataFrame(values_list)
coordinate = pd.DataFrame(coordinate)

# rename the columns name
reference = reference.rename(columns={0:'Photo Reference 1', 1:'Photo Reference 2', 2:'Photo Reference 3',\
                   3:'Photo Reference 4', 4:'Photo Reference 5', 5:'Photo Reference 6',\
                   6:'Photo Reference 7', 8:'Photo Reference 9', 9:'Photo Reference 10', \
                   10:'Photo Reference 11', 11:'Photo Reference 12', 12:'Photo Reference 13',\
                   13:'Photo Reference 14', 14:'Photo Reference 15', 15:'Photo Reference 16',\
                   16:'Photo Reference 17',17:'Photo Reference 18', 18:'Photo Reference 19', 19:'Photo Reference 20'})
coordinate = coordinate.rename(columns={'lat':'Lat', 'lng': 'Lag'})

# Add new cloumns to original data
data[coordinate.columns] = coordinate
data[reference.columns] = reference

# save data as a csv file
data.to_csv('new post primary school list.csv')
print("the file have been saved" + os.getcwd())
