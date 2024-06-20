from tkinter import * 
import requests

master = Tk()
master.title("Weather App")

# API endpoint
url = "https://api.openweathermap.org/data/2.5/weather?id=524901&appid=67c31cbcfaf6671ff50c95a10c177c99"

def fetchWeather(event=None):
    # Send a GET request to the API
    try:
        response = requests.get(url, params={"q": cityNameEntry.get(), "units": "metric"})
        errorMessage.set("")

        weatherData = response.json()

        cityName.set(weatherData["name"])
        countryName.set(weatherData["sys"]["country"])
        currentTemperature.set(round(weatherData["main"]["temp"]))
        maxTemperature.set(round(weatherData["main"]["temp_max"]))
        minTemperature.set(round(weatherData["main"]["temp_min"]))
        mainWeather.set(weatherData["weather"][0]["main"])
        weatherDescription.set(weatherData["weather"][0]["description"])
    except KeyError:
        errorMessage.set("This city does not exist/is not currently in the database.")

'''def fetchCities(cityName):
    response = requests.get(url, params={"q": cityName, "units": "metric"})

    weatherData = response.json()

    try:
        cities = [item["name"] for item in weatherData["list"]]

        cityListBox.delete(0, END)
        for city in cities:
            cityListBox.insert(END, city)
    except:
        pass'''


# Initialising variables for the entry of the city name
cityNameEntryLabel = Label(master, text="Enter the name of the city/region (followed by the ISO code of the country that the city is in - e.g. Rome, IT): ")
cityNameEntry = Entry(master)
cityNameEntry.bind("<Return>", fetchWeather)
errorMessage = StringVar()
entryError = Label(master, textvariable=errorMessage)
'''chosenCity = StringVar()
cityListBox = Listbox(master, listvariable=chosenCity)
cityName = cityNameEntry.get()
fetchCities(cityName)'''


# Initialising variables for the display of the city name
cityNameDisplayLabel = Label(master, text="City/region: ")
cityName = StringVar()
cityNameDisplay = Label(master, textvariable=cityName)


# Initialising variables for the display of the region name
countryNameDisplayLabel = Label(master, text="Country: ")
countryName = StringVar()
countryNameDisplay = Label(master, textvariable=countryName)


# Initialising variables for the display of the current temperature
currentTemperatureDisplayLabel = Label(master, text="Current temperature (°C): ")
currentTemperature = StringVar()
currentTemperatureDisplay = Label(master, textvariable=currentTemperature)


# Initialising variables for the display of the max temperature
maxTemperatureDisplayLabel = Label(master, text="Maximum temperature (°C): ")
maxTemperature = StringVar()
maxTemperatureDisplay = Label(master, textvariable=maxTemperature)


# Initialising variables for the display of the min temperature
minTemperatureDisplayLabel = Label(master, text="Minimum temperature (°C): ")
minTemperature = StringVar()
minTemperatureDisplay = Label(master, textvariable=minTemperature)


# Initialising variables for the display of the main weather
mainWeatherLabel = Label(master, text="Main weather:")
mainWeather = StringVar()
mainWeatherDisplay = Label(master, textvariable=mainWeather)
# NB: eventually replace 'main weather' with an icon of the current weather


# Initialising variables for the display of the weather description
weatherDescriptionLabel = Label(master, text="Description: ")
weatherDescription = StringVar()
weatherDescriptionDisplay = Label(master, textvariable=weatherDescription)


# Grid layout organisation
cityNameEntryLabel.grid(row=0, column=0)
cityNameEntry.grid(row=0, column=1)
entryError.grid(row=1, column=1)
#cityListBox.grid(row=1,column=0)

cityNameDisplayLabel.grid(row=2, column=0)
cityNameDisplay.grid(row=2, column=1)

countryNameDisplayLabel.grid(row=3, column=0)
countryNameDisplay.grid(row=3, column=1)

currentTemperatureDisplayLabel.grid(row=4, column=0)
currentTemperatureDisplay.grid(row=4, column=1)

maxTemperatureDisplayLabel.grid(row=5, column=0)
maxTemperatureDisplay.grid(row=5, column=1)

minTemperatureDisplayLabel.grid(row=6, column=0)
minTemperatureDisplay.grid(row=6, column=1)

mainWeatherLabel.grid(row=7, column=0)
mainWeatherDisplay.grid(row=7, column=1)

weatherDescriptionLabel.grid(row=8,column=0)
weatherDescriptionDisplay.grid(row=8,column=1)

# Main loop of the screen
master.mainloop()