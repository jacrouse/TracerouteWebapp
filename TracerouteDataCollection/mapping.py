import folium
import csv
from pandas import *
from colorhash import ColorHash


def mapping(m, dest, coordinates):
    #generate unique color from destination string
    hexColor = ColorHash(dest).hex
    folium.PolyLine(coordinates, tooltip="Path", color=hexColor).add_to(m)
    
    m.save("index.html")


def correctForDistance(coordinates):
    #test whether to add 360 to longitude by finding euclidean distance
    #between two nodes, i.e. the first tuple of coords compared to the next


def coordsToTuple(strCoords):
    #remove undesirable characters
    formatted = ''.join(c for c in strCoords if c not in "[],")

    #dont include irregular coordinates
    if "NoLat" in formatted:
        return None

    #convert to float and return
    floatedList = list(map(float, formatted.split(' ')))

    return tuple(floatedList)    


def main():
    #instantiate map
    m = folium.Map(location=(50, 0), zoom_start=8)

    data = read_csv("recordedRoutes.csv")
    destinations = data["Destination"].to_list()
    coordinates = data["Coords"].to_list()
    
    #use first destination as reference after zipping two lists
    both = tuple(zip(destinations, coordinates))
    currentDest = both[0][0]

    #keep track of current coordinates to plot a path
    coordsToPlot = []
    
    #iterate through both
    for destAndCoords in both:
        if destAndCoords[0] == currentDest:
            tupelizedCoords = coordsToTuple(destAndCoords[1])
            if(tupelizedCoords != None):
                coordsToPlot.append(coordsToTuple(destAndCoords[1]))
        else:
            #plot current path
            mapping(m, currentDest, coordsToPlot)
            
            #reset current coordinates to plot
            coordsToPlot = []
            tupelizedCoords = coordsToTuple(destAndCoords[1])
            if(tupelizedCoords != None):
                coordsToPlot.append(coordsToTuple(destAndCoords[1]))
                
            currentDest = destAndCoords[0]

if __name__ == "__main__":
    main()
