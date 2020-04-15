import sys
import requests
import mysql.connector
from mysql.connector import Error
import GetData.config as c

def main():

    try:
        # Connect to database and create schema if not existing
        connection = mysql.connector.connect(host=c.host, user=c.user, password=c.password)
        cursor = connection.cursor()
        createSchema = "CREATE DATABASE IF NOT EXISTS " + c.db_name + ";"
        cursor.execute(createSchema)

        if (connection.is_connected()):
            cursor.close()
            connection.close()

    except:
        print("Error: Could not create database schema")
        print("Aborted")

        # exit the program
        sys.exit()

    def currentWeather():
        """Function to call weather get weather data from api """

        try:
            url = 'http://api.openweathermap.org/data/2.5/weather?lat=53.3498&lon=-6.2603&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'
            response = requests.get(url)

            # if connection failed
            if response.status_code != 200:
                print("Error: connection failed!")
                print("Aborted")

            data = response.json()
            # try to connect to database

        except:
            print("Error: connection failed!")
            sys.exit()

        try:
            tblName = "weatherDynamic"

            # connection to database
            connection = mysql.connector.connect(host=c.host, database=c.db_name, user=c.user, password=c.password)

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
                        Timestamp CHAR(10) NOT NULL,
                        PRIMARY KEY (wID,Timestamp))"""

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

        # exception if connection failed
        except Error as e:
            print("Error while connecting to MySQL", e)
            print("Aborted")

    currentWeather()


if __name__ == '__main__':
    main()
