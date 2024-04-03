import folium
import csv
from pandas import *
from colorhash import ColorHash


def mapping(m, dest, coordinates):
    #generate unique color from destination string
    hexColor = ColorHash(dest).hex

    #coordinates must be a tuple
    folium.PolyLine(tuple(coordinates), tooltip="Path", color=hexColor).add_to(m)
    
    m.save("index.html")


def correctForDistance(coordinates):
    return coordinates


def coordsToTuple(strCoords):
    #remove undesirable characters
    formatted = ''.join(c for c in strCoords if c not in "[],")

    #dont include irregular coordinates
    if "NoLat" in formatted:
        return None

    #convert to float and return as a list
    return list(map(float, formatted.split(' ')))


def euclideanDistance(coordinates):
    return


def main():
    #instantiate map
    m = folium.Map(location=(50, 0), zoom_start=8)

    data = read_csv("recordedRoutes.csv")
    destinations = data["Destination"].to_list()

    #extract raw coordinate strings
    coordinatesPreProcessing = data["Coords"].to_list()
    #process weird characters out of them and turn them into a clean list
    coordinatesPreCorrection = [coordsToTuple(item) for item in coordinatesPreProcessing]
    #lastly, correct them for shortest path
    coordinates = correctForDistance(coordinatesPreCorrection)
    
    #use first destination as reference after zipping two lists
    both = tuple(zip(destinations, coordinates))
    currentDest = both[0][0]

    #keep track of current coordinates to plot a path
    coordsToPlot = []
    
    #iterate through both
    for destAndCoords in both:
        if destAndCoords[1] != None:
            if destAndCoords[0] == currentDest:
                coordsToPlot.append(destAndCoords[1])
            else:
                #plot current path
                mapping(m, currentDest, coordsToPlot)
                
                #reset current coordinates to plot
                coordsToPlot = []
                coordsToPlot.append(destAndCoords[1])
                    
                currentDest = destAndCoords[0]

if __name__ == "__main__":
    main()
