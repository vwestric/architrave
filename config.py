#Configuration
class Config():
    #Custom Python Module: https://gitlab.rlp.net/vwestric/custom.git
    #Libraries
    from function_definitions import helper as useful

    #Directories
    INPUT   = "data/input/"
    OUTPUT  = "data/output/"
    TMP     = "data/tmp/"
    REGISTRY = INPUT + "register/"
    EDITIONS = INPUT + "editions/"


    #Files
    ##INPUT
    places = "places.xml"
    csvRegistry = "PlacesRegister_current.csv"

    #TMP
    visits = "visits.json"
    visitsParis = "visitsParis.json"
    visitsEurope = "visitsEurope.json"
    visitsGeoJSON = "visits.geojson"
    visitsEuropeGeolocated = "visitsEuropeGeolocated.geojson"
    visitsParisGeolocated = "visitsParisGeolocated.geojson"
    featureCollectionLineStrings = "featureCollectionLineStrings.geojson"
    numberedFeatureCollection = "numberedFeatureCollection.geojson"
    geoData = "geoData.json"
    itinerary = "itinerary.json"
    missingNumbers = "missingNumbers.csv"

    #OUTPUT
    


    #Global Variables
    featureCollection = {
                        "type": "FeatureCollection",
                        "features": []
                        }

    point = {
        "type": "Feature",
        "properties": {
            "visitor": "",
            "color": "",
            "type": ""
        },
        "geometry": {
            "type": "Point",
            "coordinates": []
        }
    }
    