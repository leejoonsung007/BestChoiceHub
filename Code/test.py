import googlemaps


KEY = "AIzaSyCEBOzLLAqOOLuQHQ8e0wEnpHXWh1NMXQA"
gmaps = googlemaps.Client(key=KEY)

result = gmaps.geocode("dublin")
for i in result:
    print(i)

