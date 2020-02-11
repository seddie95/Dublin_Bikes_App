import requests
import json

# global variables
# create a new csv file to store the data
file = open("bike_data.csv", "w")


class BikeData():
    def __init__(self):
        self.getBikeData()

    def currentWeather(self, lat, lng):
        """Function to call weather get weather data fom api """
        url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lng + '&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'
        response = requests.get(url)

        data = response.json()

        # create variables to store the json information
        temp = str(int(data['main']['temp'])) + "°c "
        minimum = str(data['main']['temp_min']) + "°c "
        maximum = str(data['main']['temp_max']) + "°c "
        description = data['weather'][0]['description'].capitalize()

        # write the temperature data to the csv
        file.write("," + temp + "," + minimum + "," + maximum + "," + description + "\n")

    def getBikeData(self):
        """Function to requests and Parse Dubline bike json data"""
        # set url avriable to the json link
        url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=385fba26ba47521eaa2c4c81e0428103ab00bc13"

        # use the requests library to request the data from the url
        r = requests.get(url)

        # use the json library to parse the url
        data = json.loads(r.text)

        # create the headers for the csv
        file.write("Number," + "Adress," + "lat," + "Long,"
                   + "Banking," + "Bike Stands," + "Available Spaces,"
                   + "Available bikes," + "Status,"
                   + "Temperature," + "Max," + "Min,"
                   + "Description\n")

        # loop through the data to extract the relevant fields
        for i in range(len(data)):
            stopNumber = str(data[i]["number"])
            address = data[i]["address"]
            banking = str(data[i]["banking"])
            bike_stands = str(data[i]["bike_stands"])
            available_bs = str(data[i]["available_bike_stands"])
            available_bikes = str(data[i]["available_bikes"])
            status = data[i]["status"]

            # get the lat and long coordinates
            position = data[i]["position"]
            lat = str(position["lat"])
            lng = str(position["lng"])

            # Write the data to the csv file
            file.write(stopNumber + "," + address + "," + lat + "," + lng + ","
                       + banking + "," + bike_stands + "," + available_bs + ","
                       + available_bikes + "," + status)

            # get weather for each stop using coordinates
            self.currentWeather(lat, lng)

        # close the file

        print("Finished")


if __name__ == '__main__':
    bike = BikeData()



