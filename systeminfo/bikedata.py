import requests
import json
from datetime import datetime
import pymysql

# RDS Connection credentials
REGION = 'us-east-1'
rds_host = "comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
name = "comp30830"
password = "password"
db_name = "comp30830"

# variable to store id of row
idNum = 0


def getBikeData():
    """Function to requests and Parse Dublin bike json data"""
    # set url variable to the json link
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=385fba26ba47521eaa2c4c81e0428103ab00bc13"

    # use the requests library to request the data from the url
    r = requests.get(url)

    # use the json library to parse the url
    data = json.loads(r.text)

    # Time information
    currTime = str(datetime.now().strftime("%H:%M"))
    day = str(datetime.now().strftime('%A'))
    date = str(datetime.now().strftime("%d/%m/%y"))

    # loop through the data to extract the relevant fields
    for i in range(len(data)):
        stopNumber = str(data[i]["number"])
        bike_stands = str(data[i]["bike_stands"])
        available_bs = str(data[i]["available_bike_stands"])
        available_bikes = str(data[i]["available_bikes"])
        status = data[i]["status"]
        global idNum
        idNum += 1

        # open up connection to mysql database on RDS
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("""insert into bike_data (bID,Stop_Number,Bike_Stands,Available_Spaces,Available_bikes,Status,Day,Date,Time)
                        values(%s,%s,%s,%s,%s,'%s','%s','%s','%s')""" % (
                        idNum, stopNumber, bike_stands, available_bikes, available_bs, status, day, date, currTime))
            conn.commit()
            cur.close()

    print("Finished")


if __name__ == '__main__':
    getBikeData()

print(idNum)
