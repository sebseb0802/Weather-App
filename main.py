from tkinter import * 
import requests
import urllib.request
import io
from PIL import Image, ImageTk
import pycountry


# Setting up the tkinter window
master = Tk()
master.title("Weather App")
master.configure(background="light blue")

# API endpoint
url = "https://api.openweathermap.org/data/2.5/weather?id=524901&appid=67c31cbcfaf6671ff50c95a10c177c99"

def fetchWeather(event=None):
    # Try and send a GET request to the API
    try:
        countryEntered = pycountry.countries.get(name = countryNameEntry.get())
        countryDataGet = f"{cityNameEntry.get()}" + ", " + f"{countryEntered.alpha_2}"

        # Use the cityName currently in the entry box to fetch information on that city (using the get() function, which returns the value of the entry box)
        response = requests.get(url, params={"q": countryDataGet, "units": "metric"})
        errorMessage.set("")

        # Converts the JSON response to a Python dictionary
        weatherData = response.json()

        # Fetch the following data from the API
        # Assign the data of the country of the specified city to the countryInformation variable using the ISO code provided in the API
        countryInformation =  pycountry.countries.get(alpha_2 = weatherData["sys"]["country"])

        # These variables are all type StringVar(), so, their values can be "set" 
        cityName.set(weatherData["name"])
        # Get the name of the country using the data in the countryInformation variable
        countryName.set(countryInformation.name)
        currentTemperature.set(round(weatherData["main"]["temp"]))
        maxTemperature.set(round(weatherData["main"]["temp_max"]))
        minTemperature.set(round(weatherData["main"]["temp_min"]))
        mainWeather.set(weatherData["weather"][0]["main"])
        weatherDescription.set(weatherData["weather"][0]["description"])
        iconCode.set(weatherData["weather"][0]["icon"])

        # Fetch the weather icon image from the API
        iconURL = f"https://openweathermap.org/img/wn/{iconCode.get()}@2x.png"
        # Convert the raw image data to data that tkinter can use
        with urllib.request.urlopen(iconURL) as u:
            raw_data = u.read()
        im = Image.open(io.BytesIO(raw_data))
        icon = ImageTk.PhotoImage(im)
        iconDisplay.config(image=icon)
        iconDisplay.image = icon

        # Display the weather details once the city and country have been entered
        cityNameDisplayLabel.grid(row=3, column=0)
        cityNameDisplay.grid(row=3, column=1)

        countryNameDisplayLabel.grid(row=4, column=0)
        countryNameDisplay.grid(row=4, column=1)

        currentTemperatureDisplayLabel.grid(row=5, column=0)
        currentTemperatureDisplay.grid(row=5, column=1)

        maxTemperatureDisplayLabel.grid(row=6, column=0)
        maxTemperatureDisplay.grid(row=6, column=1)

        minTemperatureDisplayLabel.grid(row=7, column=0)
        minTemperatureDisplay.grid(row=7, column=1)

        mainWeatherLabel.grid(row=8, column=0)
        mainWeatherDisplay.grid(row=8, column=1)

        weatherDescriptionLabel.grid(row=9,column=0)
        weatherDescriptionDisplay.grid(row=9,column=1)

        iconDisplay.grid(row=10, column=0)

    # If the specified city/country does not exist, inform the user
    except KeyError:
        # errormessage is a StringVar() type variable, meaning that its value can be "set" using this function
        errorMessage.set("The city/country does not exist or its weather is not being monitored.")

    except AttributeError:
        errorMessage.set("The city/country does not exist or its weather is not being monitored.")


# Initialising variables for the entry of the city name
cityNameEntryLabel = Label(master, text="Enter the name of the city/region: ", background="light blue")
cityNameEntry = Entry(master, background="light blue")
# When the user presses the "return" key, the fetchWeather function is called, using the entered cityName as a parameter
cityNameEntry.bind("<Return>", fetchWeather)
# Initialising variables for the entry of the country name
countryNameEntryLabel = Label(master, text="Enter the name of the country that the city is in: ", background="light blue")
countryNameEntry = Entry(master, background="light blue")
countryNameEntry.bind("<Return>", fetchWeather)

errorMessage = StringVar()
entryError = Label(master, textvariable=errorMessage, background="light blue")


# Initialising variables for the display of the city name
cityNameDisplayLabel = Label(master, text="City/region: ", background="light blue")
cityName = StringVar()
cityNameDisplay = Label(master, textvariable=cityName, background="light blue")


# Initialising variables for the display of the region name
countryNameDisplayLabel = Label(master, text="Country: ", background="light blue")
countryName = StringVar()
countryNameDisplay = Label(master, textvariable=countryName, background="light blue")


# Initialising variables for the display of the current temperature
currentTemperatureDisplayLabel = Label(master, text="Current temperature (°C): ", background="light blue")
currentTemperature = StringVar()
currentTemperatureDisplay = Label(master, textvariable=currentTemperature, background="light blue")


# Initialising variables for the display of the max temperature
maxTemperatureDisplayLabel = Label(master, text="Maximum temperature (°C): ", background="light blue")
maxTemperature = StringVar()
maxTemperatureDisplay = Label(master, textvariable=maxTemperature, background="light blue")


# Initialising variables for the display of the min temperature
minTemperatureDisplayLabel = Label(master, text="Minimum temperature (°C): ", background="light blue")
minTemperature = StringVar()
minTemperatureDisplay = Label(master, textvariable=minTemperature, background="light blue")


# Initialising variables for the display of the weather icon
iconCode = StringVar()
iconDisplay = Label(master, background="light blue")

# Initialising variables for the display of the main weather
mainWeatherLabel = Label(master, text="Main weather:", background="light blue")
mainWeather = StringVar()
mainWeatherDisplay = Label(master, textvariable=mainWeather, background="light blue")
# NB: eventually replace 'main weather' with an icon of the current weather


# Initialising variables for the display of the weather description
weatherDescriptionLabel = Label(master, text="Description: ", background="light blue")
weatherDescription = StringVar()
weatherDescriptionDisplay = Label(master, textvariable=weatherDescription, background="light blue")


# Grid layout organisation
cityNameEntryLabel.grid(row=0, column=0)
cityNameEntry.grid(row=0, column=1)

countryNameEntryLabel.grid(row=1, column=0)
countryNameEntry.grid(row=1, column=1)

entryError.grid(row=2, column=1)

# Main loop of the screen
master.mainloop()