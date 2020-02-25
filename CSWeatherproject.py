import googlemaps
import pandas as pd
import sys
import urllib.request 
import json



def find_closest(dictionary,value):
    result = min(dictionary.keys(), key = lambda key: abs(key-value))
    return(dictionary[result])
    
    
def find_station(data):
    ##goes into API and returns the new URL for raw forecast
    ## returned data is like "https://api.weather.gov/gridpoints/TOP/31,80/stations"
    
    theJSON = json.loads(data)
    if "observationStations" in theJSON["properties"]:
        print (theJSON["properties"]["observationStations"])
        StationURL = (theJSON["properties"]["observationStations"])

    StationURLopen = urllib.request.urlopen(StationURL)
    return (StationURLopen.read())

def get_the_station(data):
    theJSON = json.loads(data)
    ##IMPORTANT in a JSON file when there's square brackets that's a list so you have to do the below line
    ## in order to make it an object again so you can parse it properly
    #this function gets all the station names and elevations and turns them into a dictionary
    stationdictionary = {}
    features = theJSON["features"]
    for i in features:
        name =  (i["properties"]["@id"])
        elevation =  (i["properties"]["elevation"]["value"])
        stationdictionary.update({elevation : name})
    
    return (stationdictionary)


def read_the_station(thestation,days):
    #time stamps look like 2017-06-06T12:53:00+00:00
    #gets the data ready for processing
    URL = thestation + "/observations"
    r = urllib.request.urlopen(URL)
    data = r.read()
    theJSON = json.loads(data)
    #goes through the data and gets the first time stamp
    features = theJSON["features"]
    dictionary = {}
    
    for i in features:
        
        timestamp = (i["properties"]["timestamp"])
        temperature = (i["properties"]["temperature"]["value"])
        dictionary.update({timestamp : temperature})
    #gets the month and day from the most recent time stamp
    currenttimestamp = list(dictionary.keys())[0]
    currentday = (currenttimestamp[8:10])
    currentmonth = (currenttimestamp[5:7])
    #clears the dictionary then makes a dictionary with only the last days of data
    dictionary = {}
    for i in features:
        timestampday = ((i["properties"]["timestamp"])[8:10])
        timestampmonth = ((i["properties"]["timestamp"])[5:7])
        pretemp = (i["properties"]["temperature"]["value"])
       #sorts out the dates we dont want and puts the rest into a the dictionary
        if timestampmonth == currentmonth and (abs(int(timestampday)-int(currentday)) < days):
            if pretemp != None:
                timestamp = (i["properties"]["timestamp"])
                temperature = (i["properties"]["temperature"]["value"])
                precipitation = ()
        dictionary.update({timestamp : temperature})
    #returns the last few days of weather data, phew!
    return(dictionary)

def count_below_zero(list):
    
    belowzero = 0
    
    
    for i in list:
        
        if int(i) < 0:
            belowzero = belowzero +1
    print("the number of times the temperature dropped below zero was", belowzero, " in", len(list))
    return belowzero
    
    
def is_it_icy(dictionary):
    
    #this is the temps in chronological order
    hours = (list(reversed(dictionary.keys())))
    temps = (list(reversed(dictionary.values())))
    #print (len(hours), " is the count")
    firstthirdtemp = temps[:(int((1/3)*len(temps)))]
    secondthirdtemp = temps[(int((1/3)*len(temps))):(int((2/3)*len(temps)))+1]
    thirdthirdtemp = temps[(int((2/3)*len(temps))):]
    
    firstthirdiciness = count_below_zero(firstthirdtemp)
    secondthirdiciness = count_below_zero(secondthirdtemp)
    thirdthirdiciness = count_below_zero(thirdthirdtemp)
    print(firstthirdiciness, secondthirdiciness, thirdthirdiciness)
    
    if temps[-1] > 32:
        return (False)
    elif secondthirdiciness <= (int(.65*thirdthirdiciness)):
        return (True)
    
    
    
def find_cord_data(data):
    ##goes into API and returns the new URL for raw forecast
    ## returned data is like "https://api.weather.gov/gridpoints/TOP/31,80/forecast"
    
    theJSON = json.loads(data)
    if "forecast" in theJSON["properties"]:
        ForecastURL = (theJSON["properties"]["forecast"])
    
    ForecastURLopen = urllib.request.urlopen(ForecastURL)
    return (ForecastURLopen.read())
def read_elevation(data):
    theJSON = json.loads(data)
    ## gets the elevation of the coordinate
    elevation = int((theJSON["properties"]["elevation"]["value"]))
    print ("The elevation is" ,elevation)
    return(int(elevation))
    #print ("The Weather.gov Projected forecast is: ")
    
    #for i in theJSON["properties"]["periods"]:
      #  names = (i.get("name", "no name available"))
      #  temperatures = (i.get("temperature", "no temperature available"))
      #  detailedforecast = (i.get("detailedForecast", "no forecast available"))
       # windspeed = (i.get("windSpeed", "no windspeed available"))
       # temperaturetrend = (i.get("temperatureTrend", "no temperature trend available"))
      #  print (names, temperatures," Degrees", detailedforecast, "\n")
def form_URL(cords):
    URL = "https://api.weather.gov/points/" + cords
    print (URL)
    return (urllib.request.urlopen(URL))

def find_cords(search):
    
    ##uses google map API to find coordinates of any vaild location, long confusing string is my 
    ##API key
    gmaps_key = googlemaps.Client(key = "API-KEY")

    geocode_result = gmaps_key.geocode(search)
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lot = geocode_result[0]["geometry"]["location"]["lng"]
    except:
        lat = None
        lot = None
    
    
    
    ##formats coordinates and puts them into a usable URL!!!!!
    return(str(lat) + "," + str(lot))



def main():
    #search = "Bend Oregon"
    
    search = input("Where would you like the forecast for?: ")
    #Uses Google API to get the coordinates of any location
    #Uses Google API to get the coordinates of any location
    cords = find_cords(search)
    print(cords)
    ##opens url then sends to find_forecast
    URLopen = form_URL(cords)
    data = URLopen.read()
    # goes into forecast link for your coordinate
    corddata = find_cord_data(data)
    #gets elevation from that data, returns it for comparrison with stations
    elevation = read_elevation(corddata)
    #gets the URL for the stations that are observing your coordinate with all the data
    Stationsdata = find_station(data)
    #gets the stations elevation and name of all the stations in the form of a dictionary
    stationdic = get_the_station(Stationsdata)
    #Determines the station with the closest elevation 
    thestation = find_closest(stationdic,elevation)
    print ("\n", "The station we'll be using is: ", thestation)
    #gets the last x days of weather history from the station
    weatherhistory = read_the_station(thestation,4)
    #Primary algorithm determining if the conditions are icy
    print(is_it_icy(weatherhistory))
if __name__ == "__main__":
    main()
