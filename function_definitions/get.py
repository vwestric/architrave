#Get Functions


#Get Place Visits
def visits(data):
    #Libraries

    #Variables
    paris = {}
    europe = {}

    #Execution
    for row in data[0:]:
        if len(row) >= 7:
            if "OK" in row[3] \
            or "Ok" in row[3]:
                if "x" in row[6]:
                    paris[row[0]] = {
                        "travelers": [element.strip() for element in row[1].split(",")],
                        "geo": {}
                    }
                elif "x" not in row[6] \
                and "x" not in row[7]:
                    europe[row[0]] = {
                        "travelers": [element.strip() for element in row[1].split(",")],
                        "geo": {}
                    }

    return paris, europe

#Function to get GeoData for Places
def geoData(data, places):
    #Libraries
    from config import Config

    #Variables

    #Data


    #Execution
    for key, value in data.items():
        #Find place
        place = places.find("place", {"xml:id": key})
        #Check if place exists
        if place != None:
            #Check if geo data exists
            if place.location.geo.text != "":

                #Place Data
                #URL
                url = place.find("idno")["xml:base"]
                #German
                name = place.find("placeName", {"type": "current", "xml:lang": "de"}).text
                description = place.find("note", {"type": "description", "xml:lang": "de"}).text
                de = "<a href='%s'><b>%s</b></a><br>%s<br><b>Reisende</b>: %s" % (url, name, description, ", ".join(value["travelers"]))
                #French
                name = place.find("placeName", {"type": "current", "xml:lang": "fra"}).text
                description = place.find("note", {"type": "description", "xml:lang": "fra"}).text
                fra = "<a href='%s'><b>%s</b></a><br>%s<br><b>Voyageurs</b>: %s" % (url, name, description, ", ".join(value["travelers"]))

                #Add Data
                value["description"] = {
                    "de": de,
                    "fra": fra
                }
                value["type"] = place["subtype"]
                value["url"] = url
                value["geo"]["lat"] = float(place.location.geo.text.split(",")[0])
                value["geo"]["long"] = float(place.location.geo.text.split(",")[1])


    return data


#Function to get Color for Travelers
def color(visitor):
    if visitor == "Sturm":
        return "#00cc00"
    elif visitor == "Knesebeck":
        return "#ff0066"
    elif visitor == "Corfey":
        return "#6699ff"
    elif visitor == "Pitzler":
        return "#ffcc00"
    elif visitor == "Neumann":
        return "#cc6600"
    elif visitor == "Harrach":
        return "#ff0000"
    elif visitor == "All":
        return "#cccccc"
    else:
        return "black"


#Data for arrowMap
def lines(filePath):
    #Libraries
    from config import Config
    from operator import itemgetter

    #Variables

    #Data
    doc = Config.useful.crawler_xml(filePath)

    #Execution
    #Get all Passing Bys
    passingBys = [
                    [passingBy["ref"].replace("plc:", ""), int(passingBy["n"])]
                    for passingBy
                    in doc.find_all("placeName", {"subtype": "passingBy"})
                ]

    #Sort and return
    return sorted(passingBys, key=itemgetter(1))





