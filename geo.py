### Author: Alistair MacDonald
### Description: Wifi based geographic lookup library
### License: MIT

import network
import wifi

from http_client import post

"""Usage
from geo import geolocate

location = geolocate()
print(str(location["lat"])+", "+str(location["lng"])+" ("+str(location["accuracy"])+")")
"""

# Lookup the geolocation online
def geolocate():

	# Get the AP list
	apList = wifi.nic().list_aps()

	# Create the json string
	geojson = "{"
	firsttime=True
	for i in apList:
		# write a seperator if not the first entry
		if (not firsttime):
			geojson += ","
		else:
			firsttime=False
		# get the bssid
		bssid = ''
		for b in i['bssid']:
			bssid += "%02x" % (b);
		# Write the signal to the cache file
		geojson += "\""+bssid+"\":"+str(-i['rssi'])
	geojson += "}"

	# Check we are connected to the wifi and (re)connect if needed
	if not wifi.is_connected():
		wifi.connect()

	# Post the json request
	url = "http://tilda.agm.me.uk/geolocate"
	response = post(url, urlencoded=("data="+geojson)).raise_for_status().json()

	# Return the result
	return response
