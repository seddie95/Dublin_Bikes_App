import pandas as pd
import joblib

def inputPreProcessing(input):
       """ Function that processes the pandas series object obtained from user input and weather forecast api and
       returns a station number and a dataframe containing the data to use as input to the predictive model"""
       station = input['Stop_Number']

       input_d = {'Temperature': input['Temperature'], 'Real_Feel': input['Real_Feel'], 'Wind_Speed': input[
              'Wind_Speed'], 'Day_Friday': 0, 'Day_Monday': 0, 'Day_Saturday': 0, 'Day_Sunday': 0,
              'Day_Thursday': 0, 'Day_Tuesday': 0, 'Day_Wednesday': 0, 'Time_00': 0, 'Time_05': 0, 'Time_06': 0,
              'Time_07': 0, 'Time_08': 0, 'Time_09': 0, 'Time_10': 0, 'Time_11': 0, 'Time_12': 0, 'Time_13': 0,
              'Time_14': 0, 'Time_15': 0, 'Time_16': 0, 'Time_17': 0, 'Time_18': 0, 'Time_19': 1, 'Time_20': 0,
              'Time_21': 0, 'Time_22': 0, 'Time_23': 0, 'Weather_Main_Clear': 0, 'Weather_Main_Clouds': 0,
              'Weather_Main_Drizzle': 0, 'Weather_Main_Fog': 0, 'Weather_Main_Mist': 0, 'Weather_Main_Rain': 0}

       # Set the relevant one-hot encoded features to 1
       date = pd.to_datetime(input['Time'], unit='s') # convert timestamp to date
       day = date.strftime("%A") # extract day of the week
       day = 'Day_' + day
       input_d[day] = 1

       time = date.strftime("%H") # extract hour
       time = 'Time_' + time
       input_d[time] = 1

       weather = 'Weather_Main_' + input['Weather_Main']
       input_d[weather] = 1

       input_df = pd.DataFrame(data=input_d, index=[0])

       return input_df, station

def makePrediction(forecast):
       """ Function that calls the data prep function, loads the model corresponding to the station selected by the
       user, runs the model and returns the predicted number of bikes available"""
       model_input, stop_num = inputPreProcessing(forecast) # process user input & weather forecast data

       # load the model corresponding to the station number required
       linreg_model = joblib.load("./models/linear_regression_model_{}.pkl".format(stop_num))
       prediction = linreg_model.predict(model_input)
       numBikes = int(round(prediction[0][0]))
       print("prediction is: ", numBikes, "bikes available")
       return numBikes