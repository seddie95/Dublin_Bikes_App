import pymysql

# conecting to RDS
REGION = 'us-east-1'

rds_host = "comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
name = "comp30830"
password = "password"
db_name = "comp30830"

# https://www.youtube.com/watch?v=kITMu17WoH4&list=PLtm3q4A2l--IEPcHhsoDpC5Yh1aLaRc0D&index=2
#
# headers for the bike data table
# (bID,Number,Bike_Stands,Available_Spaces,Available_bikes,Status,Day, Date, Time)

#(wID, Temperature, Max,Min, Real_Feel,Wind,Speed, Description,Day, Date, Time)

# all ints except status which is text,Day, Date, Time and Description

#if you could implement this line in a query to test whether the database exists and if not create it
#SELECT 1 FROM bike_data.comp30830 LIMIT 1;

#0 row(s) returned
#if bike table does not exist it will throw a similar message
#Error Code: 1146. Table 'bike_data.comp30830' doesn't exist
