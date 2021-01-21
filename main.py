#Data Conversion for the Paris Project
#Author: Victor Westrich
#%%Get Visits
#Libraries
from config import Config
#Functions
from function_definitions import get
#Data
data = Config.useful.load_data(Config.INPUT, Config.csvRegistry)
#Execution
visitsParis, visitsEurope = get.visits(data)
#Output
Config.useful.write_json(Config.TMP, Config.visitsParis, visitsParis)
Config.useful.write_json(Config.TMP, Config.visitsEurope, visitsEurope)
#%%Get GeoData
#Libraries
import geopy.distance
from config import Config
#Functions
from function_definitions import get
#Data
visitsParis = Config.useful.load_data(Config.TMP, Config.visitsParis)
visitsEurope = Config.useful.load_data(Config.TMP, Config.visitsEurope)
places = Config.useful.crawler_xml(Config.REGISTRY+Config.places)

#Add Base Layer
for key in visitsParis.keys():
    if visitsParis[key]["travelers"] != [""]:
        visitsParis[key]["travelers"].append("All")

for key in visitsEurope.keys():
    if visitsEurope[key]["travelers"] != [""]:
        visitsEurope[key]["travelers"].append("All")

#Execution
visitsParisGeolocated = get.geoData(visitsParis, places)
visitsEuropeGeolocated = get.geoData(visitsEurope, places)

#Check Distance
checked = {}
centerParis = (48.856667, 2.351667)
for key, value in visitsEuropeGeolocated.items():
    if value["geo"] != {}:
        coords = (
                    value["geo"]["lat"],
                    value["geo"]["long"]
        )
        distance = geopy.distance.distance(centerParis, coords).km

        if distance > 10:
            checked[key] = value

#Output
Config.useful.write_json(Config.TMP, Config.visitsParis, visitsParisGeolocated)
Config.useful.write_json(Config.TMP, Config.visitsEurope, checked)
#%%Transform into GeoJSON
#Libraries
from config import Config
#Functions
from function_definitions import transform
#Data
visitsParis = Config.useful.load_data(Config.TMP, Config.visitsParis)
visitsEurope = Config.useful.load_data(Config.TMP, Config.visitsEurope)
print(len(visitsParis.keys()))
print(len(visitsEurope.keys()))
#Execution
visitsParisGeoJSON = transform.geoJSON(visitsParis)
visitsEuropeGeoJSON = transform.geoJSON(visitsEurope)
#Output
Config.useful.write_json(Config.TMP, Config.visitsParisGeolocated, visitsParisGeoJSON)
Config.useful.write_json(Config.TMP, Config.visitsEuropeGeolocated, visitsEuropeGeoJSON)
#%%Geo Data Dictionary
#Libraries
from config import Config
#Variables
#Data
places = Config.useful.crawler_xml(Config.REGISTRY + Config.places)
#Execution
places = {
            place["xml:id"]: {
                                "geo": [
                                        float(element.strip())
                                        for element
                                        in place.find("location").find("geo").text.split(",")
                                    ],
                                "type": place["subtype"]
                            }
            for place
            in places.find_all("place")
            if place.has_attr("xml:id")
            and place.has_attr("type")
            and place.has_attr("subtype")
            and place["type"] == "identified"
            and place.find("location") is not None
            and place.find("location").geo is not None
            and place.find("location").geo.text != ""

        }

places = {
            key: {
                    "geo": {
                        "lat": value["geo"][0],
                        "long": value["geo"][1]
                    },
                    "type": value["type"]
            }
            for key, value
            in places.items()
        }
#Output
Config.useful.write_json(Config.TMP, Config.geoData, places)
#%%Arrow Map Data
#Libraries
import os
from config import Config

#Functions
from function_definitions import get, transform

#Variables
data = {}
#Data

#Execution
for fileName in os.listdir(Config.EDITIONS):
    traveler = fileName.strip(".xml")
    data[traveler] = get.lines(Config.EDITIONS+fileName)

numberedFeatureCollection = transform.numberedFeatureCollection(data)

#Output
Config.useful.write_json(Config.TMP, Config.itinerary, data)
Config.useful.write_json(Config.OUTPUT, Config.numberedFeatureCollection, numberedFeatureCollection)
#%%Itinerary
#Libraries
from config import Config
#Variables
itineraryIds = []
featureCollection = {
    "type": "FeatureCollection",
    "features": []
}

#Data
itinerary = Config.useful.load_data(Config.TMP, Config.itinerary)
for value in itinerary.values():
    itineraryIds.extend([
                            subValue[0]
                            for subValue
                            in value
                        ])

itineraryIds = list(set(itineraryIds))

geoData = Config.useful.load_data(Config.TMP, Config.geoData)
#Execution
for key in itineraryIds:
    if key in geoData.keys():
        geo = geoData[key]

        feature = {
            "type": "Feature",
            "properties": {
                "visitor": "All",
                "color": "#cccccc",
                "type": geo["type"],
                "id": key,
                "description": {},
                "url": ""
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    geo["geo"]["long"],
                    geo["geo"]["lat"]
                ]
            }
        }

        featureCollection["features"].append(feature)

#Output
Config.useful.write_json(Config.OUTPUT, "itinerary.geojson", featureCollection)
#%%Check Missing Numbers
#Libraries
from config import Config
#Variables
itineraryIds = []

#Data
geoData = Config.useful.load_data(Config.TMP, Config.geoData)

itinerary = Config.useful.load_data(Config.TMP, Config.itinerary)
for value in itinerary.values():
    itineraryIds.extend([
                            subValue[0]
                            for subValue
                            in value
                        ])

itineraryIds = list(set(itineraryIds))

missingNumbers = [
                    row[0]
                    for row
                    in Config.useful.load_data(Config.TMP, Config.missingNumbers)
                ]

#Execution
print("Geo Data:" + "\n")
for number in missingNumbers:
    if number not in geoData.keys():
        print(number)

print("Itinerary:" + "\n")
for number in missingNumbers:
    if number not in itineraryIds:
        print(number)
#Output
#%%