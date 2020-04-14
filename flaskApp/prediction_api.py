import pandas as pd
import joblib
import time
import requests
from datetime import datetime


def getWeatherForecast(station, prediction_date, prediction_time):
    # create the time stamp using the date and time info
    timeString = str(prediction_date + " " + prediction_time)
    timestamp = time.mktime(datetime.strptime(timeString, '%d/%m/%Y %H:%M').timetuple())

    # weather api url
    url = 'http://api.openweathermap.org/data/2.5/forecast?lat=53.3498&lon=-6.2603&appid=9da3d1abfb8e1a3677d26c96350597c3&units=metric'

    # use request to call the api and parse the json response
    response = requests.get(url)
    data = response.json()

    # create variables to store the json information
    data_list = data['list']
    temp = []
    realfeel = []
    wind_speed = []
    description = []
    times = []

    # loop through the object to retrieve the necessary weather data and place them into individual lists
    for i in range(len(data_list)):
        times.append(data_list[i]['dt'])
        temp.append(data_list[i]['main']['temp'])
        realfeel.append(data_list[i]['main']['feels_like'])
        wind_speed.append(data_list[i]['wind']['speed'])
        description.append(data_list[i]['weather'][0]['main'])

    # Append the datalists into a dictionary
    weather_data = {
        'Stop_Number': station,
        'Temperature': temp,
        'Real_Feel': realfeel,
        'Wind_Speed': wind_speed,
        'Weather_Main': description,
        'Time': times
    }
    # create a dataframe using the dictionary
    df = pd.DataFrame(weather_data)

    # find the nearest time to the timestamp
    result_index = df['Time'].sub(timestamp).abs().idxmin()
    forecast = df.iloc[result_index]

    return forecast


def inputPreProcessing(input):
    """ Function that processes the pandas series object obtained from user input and weather forecast api and
    returns a station number and a dataframe containing the data to use as input to the predictive model"""
    station = input['Stop_Number']

    input_d = {'Temperature': input['Temperature'], 'Real_Feel': input['Real_Feel'], 'Wind_Speed': input[
        'Wind_Speed'], 'Day_Monday': 0, 'Day_Saturday': 0, 'Day_Sunday': 0, 'Day_Thursday': 0, 'Day_Tuesday': 0,
               'Day_Wednesday': 0, 'Time_05': 0, 'Time_06': 0,
               'Time_07': 0, 'Time_08': 0, 'Time_09': 0, 'Time_10': 0, 'Time_11': 0, 'Time_12': 0, 'Time_13': 0,
               'Time_14': 0, 'Time_15': 0, 'Time_16': 0, 'Time_17': 0, 'Time_18': 0, 'Time_19': 0, 'Time_20': 0,
               'Time_21': 0, 'Time_22': 0, 'Time_23': 0, 'Weather_Main_Clouds': 0, 'Weather_Main_Drizzle': 0,
               'Weather_Main_Fog': 0, 'Weather_Main_Mist': 0, 'Weather_Main_Rain': 0}

    # Set the relevant one-hot encoded features to 1
    date = pd.to_datetime(input['Time'], unit='s')  # convert timestamp to date
    day = date.strftime("%A")  # extract day of the week
    if day != 'Friday': # exception for first one hot encoded value
        day = 'Day_' + day
        input_d[day] = 1

    time = date.strftime("%H")  # extract hour
    if time != '00':
        time = 'Time_' + time
        input_d[time] = 1

    if input['Weather_Main'] != 'Clear':
        weather = 'Weather_Main_' + input['Weather_Main']
        input_d[weather] = 1

    input_df = pd.DataFrame(data=input_d, index=[0])

    return input_df, station


def makePrediction(station, prediction_date, prediction_time):
    """ Function that calls the data prep function, loads the model corresponding to the station selected by the
    user, runs the model and returns the predicted number of bikes available"""
    # obtain weather forecast for time selected by user
    forecast = getWeatherForecast(station, prediction_date, prediction_time)
    model_input, stop_num = inputPreProcessing(forecast)  # process user input & weather forecast data

    # load the model corresponding to the station number required
    linreg_model = joblib.load("./models/linear_regression_model_{}.pkl".format(stop_num))
    prediction = linreg_model.predict(model_input)
    numBikes = int(round(prediction[0][0]))
    print("prediction is: ", numBikes, "bikes available")
    return numBikes
