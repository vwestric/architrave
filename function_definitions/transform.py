#Transformation Functions

#Function to Transform Visits into GeoJSON
def geoJSON(data):
    #Libraries
    from config import Config

    #Functions
    from function_definitions import get

    #Variables
    #Feature Collection to contain all Points
    featureCollection = {
                        "type": "FeatureCollection",
                        "features": []
                        }

    #Execution
    #Iterate over Visited Places
    for key, value in data.items():
        #Check if GeoData exists
        if value["geo"] != {}:
            #Iteratue over Visitors
            for visitor in value["travelers"]:
                #Get Point
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
                #Add Properties
                point["properties"]["id"] = key
                point["properties"]["description"] = {
                    "de": value["description"]["de"],
                    "fra": value["description"]["fra"]
                }
                point["properties"]["url"] = value["url"]
                point["properties"]["visitor"] = visitor
                point["properties"]["type"] = value["type"]
                point["properties"]["color"] = get.color(visitor)

                #Add Geometry
                point["geometry"]["coordinates"] = [
                    value["geo"]["long"],
                    value["geo"]["lat"]
                ]

                #Append Point to Feature Collection
                featureCollection["features"].append(point)

    #Output
    return featureCollection


#Function to create polylines for arrowMap
def featureCollectionLineStrings(data):
    #Libraries
    from config import Config
    from function_definitions import get
    #Variables
    featureCollection = {
                        "type": "FeatureCollection",
                        "features": []
                        }

    #Data
    geoData = {
                key: value["geo"]
                for key, value
                in Config.useful.load_data(Config.TMP, Config.visitsEurope).items()
              }

    geoData.update({
                key: value["geo"]
                for key, value
                in Config.useful.load_data(Config.TMP, Config.visitsParis).items()
              })

    for key, value in data.items():
        LineString = {
            "type": "Feature",
            "properties": {
                "visitor": key,
                "color": get.color(key),
                "type": ""
            },
            "geometry": {
                "type": "LineString",
                "coordinates": []
            }
        }
        for subValue in value:
            if subValue[0] in geoData.keys():
                LineString["geometry"]["coordinates"].append([
                    geoData[subValue[0]]["geo"]["long"],
                    geoData[subValue[0]]["geo"]["lat"]
                ])

        featureCollection["features"].append(LineString)

    return featureCollection


def numberedFeatureCollection(data):
    #Libraries
    from config import Config
    from function_definitions import get
    #Variables
    featureCollection = {
                        "type": "FeatureCollection",
                        "features": []
                        }

    #Data
    geoData = Config.useful.load_data(Config.TMP, Config.geoData)
    # geoData = {
    #             key: value["geo"]
    #             for key, value
    #             in Config.useful.load_data(Config.TMP, Config.visitsEurope).items()
    #           }
    #
    # geoData.update({
    #             key: value["geo"]
    #             for key, value
    #             in Config.useful.load_data(Config.TMP, Config.visitsParis).items()
    #           })

    for key, value in data.items():
        for subValue in value:
            Point = {
                "type": "Feature",
                "properties": {
                    "id": "",
                    "visitor": key,
                    "color": get.color(key),
                    "type": "",
                    "label": ""
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": []
                }
            }

            if subValue[0] in geoData.keys():
                Point["geometry"]["coordinates"] = [
                    geoData[subValue[0]]["geo"]["long"],
                    geoData[subValue[0]]["geo"]["lat"]
                ]
                Point["properties"]["label"] = numberedIcon(key, int(subValue[1]))
                Point["properties"]["id"] = subValue[0]

                featureCollection["features"].append(Point)

    return featureCollection


def numberedIcon(traveler, number):
    #Libraries
    from function_definitions import get

    #Variables
    color = get.color(traveler)

    #Execution
    if number < 10:

        return """
<svg xmlns="http://www.w3.org/2000/svg"
     width="75.6614mm" height="76.9841mm"
     viewBox="0 0 286 291">
  <path id="NumberedCircle"
        fill="%s" stroke="%s" stroke-width="1"
        d="M 141.00,0.86
           C 141.00,0.86 128.00,0.86 128.00,0.86
             119.45,1.99 109.23,4.24 101.00,6.72
             66.55,17.10 37.18,41.99 19.43,73.00
             -25.51,151.50 12.58,256.27 100.00,283.97
             118.46,289.82 138.78,291.67 158.00,289.83
             174.67,288.24 192.10,282.80 207.00,275.24
             221.99,267.65 236.58,256.46 247.83,244.00
             301.30,184.80 297.50,90.91 238.00,37.17
             225.20,25.61 210.99,16.80 195.00,10.40
             179.50,4.20 166.58,1.68 150.00,0.86
             150.00,0.86 141.00,0.86 141.00,0.86 Z" />
  <text x="80" y="225" font-family="Verdana" font-size="195"  font-weight="bold" fill="white">%d</text>
</svg>
        """ % (color, color, number)

    elif 9 < number < 100:

        return """
<svg xmlns="http://www.w3.org/2000/svg"
     width="75.6614mm" height="76.9841mm"
     viewBox="0 0 286 291">
  <path id="NumberedCircle"
        fill="%s" stroke="%s" stroke-width="1"
        d="M 141.00,0.86
           C 141.00,0.86 128.00,0.86 128.00,0.86
             119.45,1.99 109.23,4.24 101.00,6.72
             66.55,17.10 37.18,41.99 19.43,73.00
             -25.51,151.50 12.58,256.27 100.00,283.97
             118.46,289.82 138.78,291.67 158.00,289.83
             174.67,288.24 192.10,282.80 207.00,275.24
             221.99,267.65 236.58,256.46 247.83,244.00
             301.30,184.80 297.50,90.91 238.00,37.17
             225.20,25.61 210.99,16.80 195.00,10.40
             179.50,4.20 166.58,1.68 150.00,0.86
             150.00,0.86 141.00,0.86 141.00,0.86 Z" />
  <text x="7" y="220" font-family="Verdana" font-size="195" font-weight="bold" fill="white">%d</text>
</svg>
        """ % (color, color, number)

    elif 99 < number:

        return """
<svg xmlns="http://www.w3.org/2000/svg"
     width="75.6614mm" height="76.9841mm"
     viewBox="0 0 286 291">
  <path id="NumberedCircle"
        fill="%s" stroke="%s" stroke-width="1"
        d="M 141.00,0.86
           C 141.00,0.86 128.00,0.86 128.00,0.86
             119.45,1.99 109.23,4.24 101.00,6.72
             66.55,17.10 37.18,41.99 19.43,73.00
             -25.51,151.50 12.58,256.27 100.00,283.97
             118.46,289.82 138.78,291.67 158.00,289.83
             174.67,288.24 192.10,282.80 207.00,275.24
             221.99,267.65 236.58,256.46 247.83,244.00
             301.30,184.80 297.50,90.91 238.00,37.17
             225.20,25.61 210.99,16.80 195.00,10.40
             179.50,4.20 166.58,1.68 150.00,0.86
             150.00,0.86 141.00,0.86 141.00,0.86 Z" />
  <text x="9" y="190" font-family="Verdana" font-size="125"  font-weight="bold" fill="white">%d</text>
</svg>
        """ % (color, color, number)




