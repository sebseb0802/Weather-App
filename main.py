# For setting up the GUI as a whole
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# For displaying the weather icon + for rendering the temperature meter correctly
from PIL import Image, ImageTk

# For displaying the weather icon
import urllib.request
import io

# For rendering the temperature meter correctly
Image.CUBIC = Image.BICUBIC

# For initiating the GET request to the API
import requests

# For being able to convert between country names and ISO country codes
import pycountry


# Setting up the main window
master = ttk.Window(title="Weather App", themename="superhero")
master.state("zoomed")
master.update()

windowWidth = master.winfo_width()
windowHeight = master.winfo_height()

# API endpoint
url = "https://api.openweathermap.org/data/2.5/weather?id=524901&appid=67c31cbcfaf6671ff50c95a10c177c99"

nTabs = 0

"""backgroundImage = ttk.PhotoImage("pexels-francesco-ungaro-281260.jpg")
backgroundLabel = ttk.Label(master, image=backgroundImage)
backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)"""

#C = ttk.Canvas(master, bg="blue", height=250, width=150)
#originalBgImage = Image.open("pexels-francesco-ungaro-281260.jpg")
#resizedBgImage = originalBgImage.resize((windowWidth, windowHeight))

#bgFile = ImageTk.PhotoImage(resizedBgImage)
#master.bgfile = bgFile

#bg = ttk.Label(master, image=bgFile)
#bg.place(x=0, y=0, relwidth=1, relheight=1)

def fetchWeather(event=None):
    # Try and send a GET request to the API
    try:
        # Converts the entered country name into its ISO country code
        countryEntered = pycountry.countries.get(name = countryNameEntry.get())

        # Concatenates the entered city name and the country's ISO country code to form one string
        cityDataGet = f"{cityNameEntry.get()}" + ", " + f"{countryEntered.alpha_2}"

        # Uses the concatenated string to perform a GET request to the API
        response = requests.get(url, params={"q": cityDataGet, "units": "metric"})

        # Sets the errorMessage variable to a placeholder blank
        errorMessage.set("")

        # Converts the JSON response to a Python dictionary
        weatherData = response.json()

        # Fetch the following data from the API
        # Assign the data of the country of the specified city to the countryInformation variable using the ISO country code provided in the API
        countryInformation =  pycountry.countries.get(alpha_2 = weatherData["sys"]["country"])

        # Changes the colour of the temperature meter based on if the current temperature fetched from the API is within a certain range
        if weatherData["main"]["temp"] >= 25:
            meterStyle = DANGER
        elif weatherData["main"]["temp"] <= 24 and weatherData["main"]["temp"] >= 18:
            meterStyle = WARNING
        elif weatherData["main"]["temp"] <= 17 and weatherData["main"]["temp"] >= 12:
            meterStyle = SUCCESS
        elif weatherData["main"]["temp"] <= 11 and weatherData["main"]["temp"] >= 5:
            meterStyle = INFO
        else:
            meterStyle = PRIMARY

        # Create the temperature meter
        temperatureMeter = ttk.Meter(
            metertype="semi",
            metersize=150, 
            amountused=round(weatherData["main"]["temp"]),
            amountmin=round(weatherData["main"]["temp_min"])-2,
            amountmax=round(weatherData["main"]["temp_max"])+2,
            subtext="°C",
            textleft=round(weatherData["main"]["temp_min"])-2,
            textright=round(weatherData["main"]["temp_max"])+2,
            wedgesize=10,
            bootstyle=meterStyle
            )
        
        """global nTabs
        nTabs += 1
        global newTab
        weatherTabs.add(newTab, text=f"{nTabs}")"""

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
        temperatureMeter.grid(row=10, column=1)

        #weatherTabs.grid(row=11, column=0)

    # If the specified city/country does not exist, inform the user
    except KeyError:
        # errorMessage is a StringVar() type variable, meaning that its value can be "set" using this function
        errorMessage.set("The city/country does not exist or its weather is not being monitored.")

    except AttributeError:
        errorMessage.set("The city/country does not exist or its weather is not being monitored.")


#weatherTabs = ttk.Notebook(master)
#newTab = ttk.Frame(weatherTabs)

# Initialising variables for the entry of the city name
cityNameEntryLabel = ttk.Label(master, text="Enter the name of the city/region: ")



cityNameEntry = ttk.Entry(master)
# When the user presses the "return" key, the fetchWeather function is called, using the entered cityName as a parameter
cityNameEntry.bind("<Return>", fetchWeather)
# Initialising variables for the entry of the country name
countryNameEntryLabel = ttk.Label(master, text="Enter the name of the country that the city is in: ")
countryNameEntry = ttk.Entry(master)
countryNameEntry.bind("<Return>", fetchWeather)

errorMessage = ttk.StringVar()
entryError = ttk.Label(master, textvariable=errorMessage)


# Initialising variables for the display of the city name
cityNameDisplayLabel = ttk.Label(master, text="City/region: ")
cityName = ttk.StringVar()
cityNameDisplay = ttk.Label(master, textvariable=cityName, )


# Initialising variables for the display of the region name
countryNameDisplayLabel = ttk.Label(master, text="Country: ")
countryName = ttk.StringVar()
countryNameDisplay = ttk.Label(master, textvariable=countryName)


# Initialising variables for the display of the current temperature
currentTemperatureDisplayLabel = ttk.Label(master, text="Current temperature (°C): ")
currentTemperature = ttk.StringVar()
currentTemperatureDisplay = ttk.Label(master, textvariable=currentTemperature)


# Initialising variables for the display of the max temperature
maxTemperatureDisplayLabel = ttk.Label(master, text="Maximum temperature (°C): ")
maxTemperature = ttk.StringVar()
maxTemperatureDisplay = ttk.Label(master, textvariable=maxTemperature)


# Initialising variables for the display of the min temperature
minTemperatureDisplayLabel = ttk.Label(master, text="Minimum temperature (°C): ")
minTemperature = ttk.StringVar()
minTemperatureDisplay = ttk.Label(master, textvariable=minTemperature)


# Initialising variables for the display of the weather icon
iconCode = ttk.StringVar()
iconDisplay = ttk.Label(master)

# Initialising variables for the display of the main weather
mainWeatherLabel = ttk.Label(master, text="Main weather:")
mainWeather = ttk.StringVar()
mainWeatherDisplay = ttk.Label(master, textvariable=mainWeather)
# NB: eventually replace 'main weather' with an icon of the current weather


# Initialising variables for the display of the weather description
weatherDescriptionLabel = ttk.Label(master, text="Description: ")
weatherDescription = ttk.StringVar()
weatherDescriptionDisplay = ttk.Label(master, textvariable=weatherDescription)


# Grid layout organisation
cityNameEntryLabel.grid(row=0, column=0)
cityNameEntry.grid(row=0, column=1)

countryNameEntryLabel.grid(row=1, column=0)
countryNameEntry.grid(row=1, column=1)

entryError.grid(row=2, column=1)
#C.grid(row=2, column=4)

# Main loop of the screen
master.mainloop()