'''
Created on 13 Feb 2020

@author: Dennis Kroner
'''


def main():
    
    import requests
    import json
    from datetime import datetime
    import sys
    import mysql.connector
    from mysql.connector import Error
    
    # RDS Connection credentials
    host = "localhost"
    user = "root"
    password = "password"
    db_name = "Project"
    
    def getBikeData():
        """Function to requests and Parse Dublin bike json data"""
            
        # set url variable to the json link
        url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=4b6c99a317e1d320347b512f9262a0622815dcc2"
    
        # use the requests library to request the data from the url
        r = requests.get(url)
    
        # if connection failed
        if r.status_code != 200:   
            print("Error: connection failed!")
            print("Aborted")
             
            # exit the program
            sys.exit()
        # use the json library to parse the url
        data = json.loads(r.text)

        return data
    
    def getWeatherData():
        """Function to requests and Parse weather data"""
             
        # set url variable to the json link
        url = "http://api.openweathermap.org/data/2.5/forecast?id=2964574&APPID=dfd1e90170a1d337dc48f8b3da06bbb1"
     
        # use the requests library to request the data from the url
        r = requests.get(url)
  
        # if connection failed
        if r.status_code != 200:   
            print("Error: connection failed!")
            print("Aborted")
              
            # exit the program
            sys.exit()
        # use the json library to parse the url
        data = json.loads(r.text)
 
        return data
     
    
    def updateDynBikeTbl(data):
        """Function to update dynamic bike date in DB"""
        
        # try to connect to database
        try:
            tblName = "BikeDynamic"
               
            # connection to database
            connection = mysql.connector.connect(host=host, database=db_name, user=user, password=password)
               
            # if successfully connected
            if connection.is_connected():
                # SQL query to check if table exists
                tblExists = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '"+ tblName +"'"
       
                # execute SQL query
                cursor = connection.cursor()
                cursor.execute(tblExists)
                   
                # if table does not yet exist
                if cursor.fetchone() is None:
                    # prepare SQL query
                    createTable = """CREATE TABLE """+ tblName +""" ( 
                        Stop_Number INT NOT NULL,
                        Bike_Stands INT NOT NULL,
                        Available_Spaces INT NOT NULL,
                        Available_Bikes INT NOT NULL,
                        Station_Status VARCHAR(6) NOT NULL,
                        Last_Update_Day VARCHAR(9) NOT NULL,
                        Last_Update_Date DATE NOT NULL,
                        Last_Update_Time TIME NOT NULL,
                        PRIMARY KEY (Stop_Number, Last_Update_Date, Last_Update_Time))"""
            
                    # execute SQL query
                    cursor = connection.cursor()
                    cursor.execute(createTable)
                           
                # loop through the data to extract the relevant fields
                for val in data:
                    stopNumber = str(val["number"])
                    bike_stands = str(val["bike_stands"])
                    available_bs = str(val["available_bike_stands"])
                    available_bikes = str(val["available_bikes"])
                    status = val["status"]
                    
                    ts = val['last_update']/1000
                    day = datetime.utcfromtimestamp(ts).strftime('%A')
                    currTime = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')
                    date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
         
                    insertTable = """INSERT INTO """+ tblName +""" (Stop_Number,Bike_Stands,
                                    Available_Spaces,Available_bikes,Station_Status,Last_Update_Day,Last_Update_Date,Last_Update_Time) 
                                    VALUES (%s,%s,%s,%s,'%s','%s','%s','%s')""" % (stopNumber,
                                    bike_stands, available_bikes, available_bs, status, day, date, currTime)
          
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
            sys.exit()


    def updateStatBikeTbl(data):
        """Function to update dynamic bike date in DB"""
        
        # try to connect to database
        try:
            tblName = "BikeStatic"
               
            # connection to database
            connection = mysql.connector.connect(host=host, database=db_name, user=user, password=password)
               
            # if successfully connected
            if connection.is_connected():
                # SQL query to check if table exists
                tblExists = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '"+ tblName +"'"
       
                # execute SQL query
                cursor = connection.cursor()
                cursor.execute(tblExists)
                   
                # if table does not yet exist
                if cursor.fetchone() is None:
                    # prepare SQL query
                    createTable = """CREATE TABLE """+ tblName +""" ( 
                        Stop_Number INT NOT NULL,
                        Contract_Name VARCHAR(6) NOT NULL,
                        Stop_Name VARCHAR(45) NOT NULL,
                        Stop_Address VARCHAR(45) NOT NULL,
                        Pos_Lat VARCHAR(45) NOT NULL,
                        Pos_Lng VARCHAR(45) NOT NULL,
                        Banking VARCHAR(5) NOT NULL,
                        PRIMARY KEY (Stop_Number))"""
            
                    # execute SQL query
                    cursor = connection.cursor()
                    cursor.execute(createTable)
                           
                # loop through the data to extract the relevant fields
                for val in data:
                    stopNumber = str(val["number"])
                    contract_name = str(val["contract_name"])
                    stop_name = str(val["name"])
                    stop_address = str(val["address"])
                    pos_lat = val["position"]["lat"]
                    pos_lng = val["position"]["lng"]
                    banking = str(val["banking"])
                    
                    insertTable = """INSERT INTO """+ tblName +""" (Stop_Number,Contract_Name,
                                    Stop_Name,Stop_Address,Pos_Lat,Pos_Lng,Banking) 
                                    VALUES ('%s','%s','%s','%s','%s','%s','%s')""" % (stopNumber,
                                    contract_name, stop_name, stop_address, pos_lat, pos_lng, banking)
          
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
            sys.exit()
#         
#     # function call to get data from JCDecaux
#     data = getBikeData()
#     
#     # function call to fill DB with dynamic data
#     updateDynBikeTbl(data)
#     
#     # function call to fill DB with static data
#     updateStatBikeTbl(data)
    
    getWeatherData()
            
if __name__ == '__main__':
    main()
    print("Finished")
