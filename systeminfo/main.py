import requests
import json

# create a new csv file to store the data
file = open("bike_data.csv", "w")


def currentWeather(lat, lng):
    """Function to call weather get weather data fom api """
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lng + '&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'
    response = requests.get(url)

    data = response.json()

    # create variables to store the json information
    temp = str(data['main']['temp'])
    realfeel = str(int(data['main']['feels_like']))
    minimum = str(data['main']['temp_min'])
    maximum = str(data['main']['temp_max'])
    description = data['weather'][0]['description'].capitalize()
    wind_speed = str(data['wind']['speed'])

    # write the temperature data to the csv
    file.write("," + temp + "," + minimum + "," + maximum
               + "," + realfeel + "," + wind_speed + "," + description + "\n")


def getBikeData():
    """Function to requests and Parse Dublin bike json data"""
    # set url avriable to the json link
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=385fba26ba47521eaa2c4c81e0428103ab00bc13"

    # use the requests library to request the data from the url
    r = requests.get(url)

    # use the json library to parse the url
    data = json.loads(r.text)

    # create the headers for the csv
    file.write("Number," + "Bike Stands,"
               + "Available Spaces,"
               + "Available bikes," + "Status,"
               + "Temperature," + "Max,"
               + "Min," + "Real Feel,"
               + "Wind Speed," + "Description\n")

    # loop through the data to extract the relevant fields
    for i in range(len(data)):
        stopNumber = str(data[i]["number"])
        bike_stands = str(data[i]["bike_stands"])
        available_bs = str(data[i]["available_bike_stands"])
        available_bikes = str(data[i]["available_bikes"])
        status = data[i]["status"]

        # get the lat and long coordinates
        position = data[i]["position"]
        lat = str(position["lat"])
        lng = str(position["lng"])

        # Write the data to the csv file
        file.write(stopNumber + "," + bike_stands + "," + available_bs + ","
                   + available_bikes + "," + status)

        # call currentWeather function to get weather for each stop using coordinates
        currentWeather(lat, lng)

    # close the file
    file.close()
    print("Finished")

if __name__ == '__main__':
    getBikeData()
