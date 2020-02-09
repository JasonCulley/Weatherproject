# Weatherproject
A JSON parser with an algorithm and GUI

Criteria A

Client:
A parent
Advisor:
A longtime family friend who’s a very experienced software engineer
Problem:
Based on our conversation, as cited in appendix A, my client states that the problem they
have is difficulty finding snow conditions for cross country ski resorts. During the winter, my
client likes to go cross-country skiing with his friends and family, this differs from downhill skiing
in a number of ways but the most logistically challenging way is that you need to ski at lower
altitudes, and detailed snow reports for these altitudes doesn’t really exist. He wants an
application of some sort that can look at specific ski resorts and supply an adequate weather
report, including current snow build-up, snow buildup over the last seven days, average
temperature over the last seven days, current wind speeds, today's precipitation.
Product:
A desktop script written in C++ that serves as a web scraper that interacts with weather
service APIs and supplies an adequate weather report.
Justification:
The point of creating a computer program to complete a task is to save time and
perform calculations that a human could not accomplish. This product does both of those things.
By finding the GPS coordinates of any given snow park, a task that would normally take an
intense amount of obnoxious googling, and extrapolating and organizing all of the relevant data
derived from that GPS location, the program saves a huge amount of time. Each one of those
steps would take several minutes for a human to accomplish, and that’s with only one snow
park. This program allows for multiple snowparks to be searched at the same time which
exponentially increases the data derived and time saved. The product will make it possible to
assess a large number of ideal snow parks and figure out which one has the ideal conditions for
your excursion. The convenience of entering your five favorite snow parks and instantly getting
an excellent idea of what the snow conditions will be like on any given day over having to do all
of the research on your own is huge. The data needs to be accessed on the morning of the

excursion so being able to learn everything you need to know in a few seconds instead of a half-
hour is a world of difference. I will be using C++, my justification for using C++ is I believe it will

teach me the most about the fundamentals of programming and based on my research is the
most friendly language for creating personal desktop applications.
Success Criteria:
1. Web scraper that interacts with weather service API
2. Simple readable data table displaying all relevant data to the client
3. Locates GPS of snow parks by interacting with a maps API to locate the GPS of any
given location.
4. Simple UI for entering snowpark names
5. Organizes data into an array for calculations and extrapolation.

Criterion B: Design

The function of the product as stated in Criteria A is to supply a weather report on a snowpark that may not be serviced by mainstream weather apps. In order to accomplish this, my plan is to create a web scraper that will first take a string from a search field provided to the client that will be the snow park we are looking for. Next using rather a GPS API or finding the zip code depending on how things work out, the program will get more specific information on the location of the park. Using this information it will go to the National Weather Service API and find the current snow report of the park and forecast, then use algorithms to extrapolate a more comprehensive data set for the user to analyze and factor into their decision about whether they are to go skiing.


Success Criteria Testing

Web scraper that interacts with Weather Service API

I will know whether this function is working by whether I can get any data at all from the API. I will test by just extracting one arbitrary data point

2. Simple readable data table displaying all relevant data to the client

I will know this works when there is a labeled data table that is accessible through the UI

3.Locates GPS of snow parks by interacting with a maps API to locate the GPS of any
given location.

I will know this is working when you can enter a snow park/(any location) into the search bar and it will be able to return the location that the Weather Service can use

4.Simple UI for entering snowpark names

I will know that this is completed when there is a working search field that you can type into and is clearly labeled with instructions

5.Organizes data into an array for calculations and extrapolation.

I will know when this is completed when there have been multiple data points extracted from the weather API and they are organized into a suitable data structure and using algorithms, turned into useful statistics   

UI Plans


Design Flowcharts




