import googlemaps
import pandas as pd
import sys
import urllib.request 
import json
import tkinter as tk


window = tk.Tk()
class GUI():
    def RunGUI(self):
    
        window.configure(bg ="#179de6")
        
        l1 = tk.Label(window, text = "Enter Snowpark Here: ",bg = "#179de6")
        l2 = tk.Label(window, text = "Results should come in less than ten seconds",bg = "#179de6")
        l3 = tk.Label(window, text = "API-KEY: ",bg = "#179de6")
        
        self.entSearch = tk.Entry(window,bg = "#179de6" )
        
        self.entKey = tk.Entry(window,bg = "#179de6" )
        
        self.entSearch.insert(0,"ex: Bend Oregon")
        self.entKey.insert(0,"ex: AP5asdp234...")
        
        button = tk.Button(window, text ="Finish", width = 25, command = self.end, bg = "#179de6" )


        l1.grid(row = 0, column = 0)
        l2.grid(row = 3, column = 1)
        l3.grid(row = 1, column = 0)
        
        self.entSearch.grid(row = 0, column = 1)
        self.entKey.grid(row = 1, column = 1)
        button.grid(row=2, column =1 )

        window.mainloop()
    
    def end(self):
    
        
        
        
        window1 = tk.Tk()
        
        window1.configure(bg ="#179de6")
        result = main(self.entSearch.get(), self.entKey.get())
        
        l2 = tk.Label(window1, text = result, bg = "#179de6")
        l2.grid(row = 0, column = 0)
        
        l4 = tk.Label(window1, text =("The station I am using for data is", thestation),bg = "#179de6")
        l4.grid(row = 1, column = 0)
        
        l4 = tk.Label(window1, text =("The station's elevation is ", (int(elevation)*3.28084), " feet"),bg = "#179de6")
        l4.grid(row = 2, column = 0)
        
        
        
        window.destroy()
        
        
def find_closest(dictionary,value):
    result = min(dictionary.keys(), key = lambda key: abs(key-value))
    return(dictionary[result])
    
    
def find_station(data):
    ##goes into API and returns the new URL for raw forecast
    ## returned data is like "https://api.weather.gov/gridpoints/TOP/31,80/stations"
    
    theJSON = json.loads(data)
    if "observationStations" in theJSON["properties"]:
        #print (theJSON["properties"]["observationStations"])
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
        
        if int(i) < 2:
            belowzero = belowzero +1
    #print("the number of times the temperature dropped below zero was", belowzero, " in", len(list))
    return belowzero
    
    
def is_it_icy(dictionary):
    
    #this is the temps in chronological order
    temps = (list(dictionary.values()))
  
    warm = (len(temps))- (count_below_zero(temps))
    cold = count_below_zero(temps)
    if cold == 0:
        cold = 1
    ratio = warm/cold
    
    if ratio <= (1/3):
        return("Condtions are ideal")
    elif ratio <= (2/3):
        return("Condtions are poor")
    elif ratio <= 1:
        return("Conditions are spring skiing")
    elif ratio > 1:
        return("Conditions are not fit for skiing")
    
    
    ##Compare the precentage of the time above 2C to the percentage of the time below 2C
    ##above 2C / below 2C
    ##if that ratio is below 1/3 then ideal conditions, with percipitation its snowing and great
    ##if that ratio is between 1/3 and 2/3 than poor conditions, with percipitation its terrible
    ##if its greater than 2/3 than its spring skiing, same with percipitation
    ##if no below 2C there isnt snow
    
    
    
    
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
    #print ("The elevation is" ,elevation)
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
    #print (URL)
    return (urllib.request.urlopen(URL))

def find_cords(search, KEY):
    
    ##uses google map API to find coordinates of any vaild location, long confusing string is my 
    ##API key
    gmaps_key = googlemaps.Client(key = KEY)

    geocode_result = gmaps_key.geocode(search)
    try:
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lot = geocode_result[0]["geometry"]["location"]["lng"]
    except:
        lat = None
        lot = None
    
    
    
    ##formats coordinates and puts them into a usable URL!!!!!
    return(str(lat) + "," + str(lot))



def main(search, key):
    #search = "Bend Oregon"
    
    #search = input("Where would you like the forecast for?: ")
    #Uses Google API to get the coordinates of any location
    #Uses Google API to get the coordinates of any location
    cords = find_cords(search, key)
    #print(cords)
    ##opens url then sends to find_forecast
    URLopen = form_URL(cords)
    data = URLopen.read()
    # goes into forecast link for your coordinate
    corddata = find_cord_data(data)
    #gets elevation from that data, returns it for comparrison with stations
    global elevation 
    elevation = read_elevation(corddata)
    #gets the URL for the stations that are observing your coordinate with all the data
    Stationsdata = find_station(data)
    #gets the stations elevation and name of all the stations in the form of a dictionary
    stationdic = get_the_station(Stationsdata)
    #Determines the station with the closest elevation 
    global thestation
    thestation = find_closest(stationdic,elevation)
    #print ("\n", "The station we'll be using is: ", thestation)
    #gets the last x days of weather history from the station
    weatherhistory = read_the_station(thestation,2)
    #Primary algorithm determining if the conditions are icy
    
    result = (is_it_icy(weatherhistory))
    return(result)
if __name__ == "__main__":
    firstGUI = GUI()
    firstGUI.RunGUI()
    
