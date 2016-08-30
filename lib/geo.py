### Author: Alistair MacDonald
### Description: Wifi based geographic lookup library
### License: MIT

import network
import wifi
import ujson

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
	wifiobj = {}
	for i in apList:
		# get the bssid
		bssid = ''
		for b in i['bssid']:
			bssid += "%02x" % (b);
		# Add the thtry to the list
		wifiobj.update({bssid:-i['rssi']})
	# Convert the list ot json
	wifijson = ujson.dumps(wifiobj)

	# Check we are connected to the wifi and (re)connect if needed
	if not wifi.is_connected():
		wifi.connect()

	# Post the json request
	url = "http://tilda.agm.me.uk/geolocate"
	response = post(url, urlencoded=("data="+wifijson)).raise_for_status().json()

	# Return the result
	return response

