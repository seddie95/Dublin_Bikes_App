
import requests
import json
import sys
import mysql.connector
from mysql.connector import Error

def main():
    print("Started")

    # RDS Connection credentials
    host = "comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
    user = "comp30830"
    password = "password"
    db_name = "comp30830"

    try:
        # Connect to database and create schema if not existing
        connection = mysql.connector.connect(host=host, user=user, password=password)
        cursor = connection.cursor()
        createSchema = "CREATE DATABASE IF NOT EXISTS " + db_name +";"
        cursor.execute(createSchema)
        
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            
    except:
        print("Error: Could not create database schema")
        print("Aborted")
        
        # exit the program
        sys.exit()

    def getData(url):
        """Function to requests and Parse json data"""
                 
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
                        Stop_Number INT(6) NOT NULL,
                        Bike_Stands INT NOT NULL,
                        Available_Spaces INT NOT NULL,
                        Available_Bikes INT NOT NULL,
                        Station_Status VARCHAR(6) NOT NULL,
                        Last_Update CHAR(10) NOT NULL,
                        PRIMARY KEY (Stop_Number, Last_Update))"""
             
                    # execute SQL query
                    cursor = connection.cursor()
                    cursor.execute(createTable)
                            
                # loop through the data to extract the relevant fields
                for val in data:
                    stopNumber = str(val["number"])
                    bike_stands = str(val["bike_stands"])
                    available_bs = str(val["available_bike_stands"])
                    available_bikes = str(val["available_bikes"])
                    status = str(val["status"])
                    last_update = str(val['last_update'])[:10]
          
                    insertTable = """INSERT INTO """+ tblName +""" (Stop_Number,Bike_Stands,
                                    Available_Spaces,Available_bikes,Station_Status,Last_Update) 
                                    VALUES (%s,%s,%s,%s,'%s','%s')""" % (stopNumber,
                                    bike_stands, available_bikes, available_bs, status, last_update)
           
                    try:
                        # execute SQL query
                        cursor = connection.cursor()
                        cursor.execute(insertTable)
                        connection.commit()
                    except:
                        pass

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
                        Stop_Number INT(6) NOT NULL,
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
                                    VALUES (%s,'%s',\"%s\",\"%s\",'%s','%s','%s')""" % (stopNumber,
                                    contract_name, stop_name, stop_address, pos_lat, pos_lng, banking)
           
                    try:
                        # execute SQL query
                        cursor = connection.cursor()
                        cursor.execute(insertTable)
                        connection.commit()
                    except:
                        pass

                    
        # exception if connection failed
        except Error as e:
            print("Error while connecting to MySQL", e)
            print("Aborted")
                
            # exit the program
            sys.exit()
      
      
    # set url variable to the json link
    url = "https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=4b6c99a317e1d320347b512f9262a0622815dcc2"    
      
    # function call to get data from JCDecaux
    bikeData = getData(url)
   
    # connection to database
    connection = mysql.connector.connect(host=host, database=db_name, user=user, password=password)
    
    # function call to fill DB with dynamic data
    updateDynBikeTbl(bikeData)
        
    # function call to fill DB with static data
    updateStatBikeTbl(bikeData)
                     
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("Finished")
            
if __name__ == '__main__':


    main()

