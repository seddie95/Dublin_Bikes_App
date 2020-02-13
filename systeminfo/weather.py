import requests
from datetime import datetime
import pymysql
import time

# RDS Connection credentials
REGION = 'us-east-1'
rds_host = "comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
name = "comp30830"
password = "password"
db_name = "comp30830"

# variable to store id of row
idNum = 0


def currentWeather():
    """Function to call weather get weather data fom api """
    url = 'http://api.openweathermap.org/data/2.5/weather?lat=53.3498&lon=-6.2603&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'
    response = requests.get(url)

    data = response.json()

    # Time information
    currTime = str(datetime.now().strftime("%H:%M"))
    day = str(datetime.now().strftime('%A'))
    date = str(datetime.now().strftime("%d/%m/%y"))

    # create variables to store the json information
    temp = data['main']['temp']
    realfeel = data['main']['feels_like']
    minimum = data['main']['temp_min']
    maximum = data['main']['temp_max']
    description = data['weather'][0]['description'].capitalize()
    wind_speed = data['wind']['speed']
    global idNum
    idNum += 1

    # open up connection to mysql database on RDS
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""insert into weatherData (wID,Temperature,Max,Min,Real_Feel,Wind_Speed,Description,Day,Date,Time)
                            values(%s,%s,%s,%s,%s,%s,'%s','%s','%s','%s')""" % (
            idNum, temp, maximum, minimum, realfeel, wind_speed, description, day, date, currTime))
        conn.commit()
        cur.close()

    print("Finished round: ", idNum)


if __name__ == '__main__':
    for i in range(5):
        currentWeather()
        time.sleep(10)
