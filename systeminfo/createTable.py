import pymysql

# conecting to RDS
REGION = 'us-east-1'

rds_host = "comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
name = "comp30830"
password = "password"
db_name = "comp30830"

# https://www.youtube.com/watch?v=kITMu17WoH4&list=PLtm3q4A2l--IEPcHhsoDpC5Yh1aLaRc0D&index=2
#
# headers for the table
# (Number,Bike_Stands,Available_Spaces,Available_bikes,Status)
#
# all ints except status which is text