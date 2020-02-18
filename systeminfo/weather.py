import requests
import mysql.connector
from mysql.connector import Error

# RDS Connection credentials
REGION = 'us-east-1'
host = "comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
user = "comp30830"
password = "password"
db_name = "comp30830"


def currentWeather():
    """Function to call weather get weather data fom api """
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=53.3498&lon=-6.2603&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'
    response = requests.get(url)

    # if connection failed
    if response.status_code != 200:
        print("Error: connection failed!")
        print("Aborted")

    data = response.json()
    # try to connect to database
    try:
        tblName = "weatherDynamic"

        # connection to database
        connection = mysql.connector.connect(host=host, database=db_name, user=user, password=password)

        # if successfully connected
        if connection.is_connected():
            # SQL query to check if table exists
            tblExists = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '" + tblName + "'"

            # execute SQL query
            cursor = connection.cursor()
            cursor.execute(tblExists)

            # if table does not yet exist
            if cursor.fetchone() is None:
                # prepare SQL query to create headers for the table
                createTable = """CREATE TABLE """ + tblName + """ (
                    wID INT NOT NULL AUTO_INCREMENT ,
                    Temperature Double,
                    Max Double,
                    Min Double,
                    Real_Feel Double,
                    Wind_Speed Double ,
                    Description TEXT,
                    Timestamp INT NOT NULL,
                    PRIMARY KEY (wID))"""

                print("Creating Table: " + tblName)
                cursor = connection.cursor()
                cursor.execute(createTable)

            # create variables to store the json information
            temp = data['main']['temp']
            realfeel = data['main']['feels_like']
            minimum = data['main']['temp_min']
            maximum = data['main']['temp_max']
            description = data['weather'][0]['description'].capitalize()
            wind_speed = data['wind']['speed']
            timestamp = data['dt']

            # Create SQL query to insert the data into the table
            insertTable = ("""INSERT INTO """ + tblName + """(Temperature,Max,Min,Real_Feel,Wind_Speed,
            Description,Timestamp) values(%s,%s,%s,%s,%s,'%s',%s)""" % (
                temp, maximum, minimum, realfeel, wind_speed, description, timestamp))

            try:
                # execute SQL query
                cursor = connection.cursor()
                cursor.execute(insertTable)
                connection.commit()
            except:
                pass

        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    # exception if connection failed
    except Error as e:
        print("Error while connecting to MySQL", e)
        print("Aborted")

    # exit the program
    print("Finished")


if __name__ == '__main__':
    currentWeather()
