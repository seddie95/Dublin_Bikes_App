# model_api.py - contains functions to clean & prep data and train & run model

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import joblib

def getBikeAndWeatherData():
    """Function that retrieves and joins both Weather and Dynamic Bike data from our database and returns a
    merged df joined by nearest datestamp"""

    engine = create_engine("mysql+mysqldb://comp30830:password@comp30830.cyn6ycrg3wxh.us-east-1.rds.amazonaws.com"
                           "/comp30830")
    wdf = pd.read_sql_query('''SELECT * FROM weatherDynamic ORDER BY Timestamp;''', engine)
    bdf = pd.read_sql_query('''SELECT * FROM BikeDynamic ORDER BY Last_Update;''', engine)

    #  clean up duplicate rows from weather df
    wdf.drop_duplicates(subset=['Timestamp'], inplace=True)

    # Convert timestamps from object to numeric data types in order to use the merge_asof() function
    bdf['Last_Update'] = pd.to_numeric(bdf['Last_Update'])
    wdf['Timestamp'] = pd.to_numeric(wdf['Timestamp'])

    # Remove rows in bdf that won't have any corresponding weather data (any records that we had scraped before we
    # started scraping weather data)
    bdf = bdf[bdf.Last_Update >= wdf.Timestamp.min()]

    #  Merge the two dataframes by matching on Timestamp nearest to Last_Update (using absolute distance)
    df = pd.merge_asof(bdf, wdf, left_on='Last_Update', right_on='Timestamp', direction='nearest')

    return df

def cleanPrepData(df):
    """Function that cleans and preps the data for modelling and returns a dataframe ready for training"""

    # Drop features that will never be used in the model
    df.drop(columns=['Bike_Stands', 'Min', 'Max', 'wID', 'Timestamp', 'Station_Status'], inplace=True)

    # Convert Last_Update from integer to datetime data type
    df['Last_Update'] = pd.to_datetime(df['Last_Update'], unit='s')

### THIS CAN BE CHANGED ONCE THE LOCKDOWN IS OVER AND BIKE USAGE RETURNS TO NORMAL
    # Remove rows relating to dates later than 12th March 2020
    df = df[df.Last_Update <= '2020-03-12 00:00:00']

    # Derive day of the week from date
    df['Day'] = df.Last_Update.apply(lambda x: x.strftime("%A"))
    # Add weekday vs weekend flag column
    weekend_days = ['Saturday', 'Sunday']
    df['Weekend'] = df.apply(lambda row: 'Y' if row['Day'] in weekend_days else 'N', axis=1)
    # Add a column to fit the precise timestamps into a reduced number of timeslots
    df['Time'] = df.Last_Update.apply(lambda x: x.strftime("%H"))
    # Drop rows with times between 1:00 and 4:59
    excluded_times = ['01', '02', '03', '04']
    df = df[df['Time'].isin(excluded_times) == False]

    def groupWeather(w_desc):
        """ Function to match lower level weather descriptions to the higher level categories available from the
        OpenWeather API"""
        atmosphere_lc = ['mist', 'tornado', 'fog', 'sand']
        atmosphere_c = ['Mist', 'Tornado', 'Fog', 'Sand']
        if 'thunderstorm' in w_desc:
            w_main = 'Thunderstorm'
        elif 'drizzle' in w_desc or 'Drizzle' in w_desc:
            w_main = 'Drizzle'
        elif 'snow' in w_desc or 'sleet' in w_desc:
            w_main = 'Snow'
        elif 'rain' in w_desc:
            w_main = 'Rain'
        elif 'cloud' in w_desc:
            w_main = 'Clouds'
        elif w_desc == 'clear sky' or w_desc == 'Clear sky':
            w_main = 'Clear'
        elif 'dust' in w_desc:
            w_main = 'Dust'
        elif 'ash' in w_desc:
            w_main = 'Ash'
        elif w_desc in atmosphere_lc:
            w_main = w_desc.capitalize()
        elif w_desc in atmosphere_c:
            w_main = w_desc
        elif w_desc == 'squalls':
            w_main = 'Squall'
        else:
            w_main = 'None'
        return w_main

    # To reduce cardinality of Description feature. This will be used in the model instead of Description as it does not
    # affect accuracy of the predictions
    df['Weather_Main'] = df.Description.apply(groupWeather)

    return df

def predictBikeAvailability(df):
    """ Function that trains models for each bike station number using a series of datasets obtained from splitting
    the training and testing data repeatedly using time series cross-validation. Saves a pickled file of the
    last (best) model for each stop number and returns a df containing all the metrics of all the models trained for
    each stop number"""
    # get full list of stop numbers
    stop_numbers = df.Stop_Number.unique()

    # lists to keep track of result metrics
    rmse_list = []
    mae_list = []
    r2_list = []
    stations_list = []

    for station in stop_numbers:
        dfm = df[df.Stop_Number == station].reset_index()
        dfm['Stop_Number'] = pd.to_numeric(dfm['Stop_Number'])
        # Drop weather description and weekend flag. Can be added back later if they are found to be meaningful once
        # more data is available
        dfm = dfm.drop(['Description', 'Weekend'], 1)
        dfm = pd.get_dummies(dfm)  # one-hot encoding of categorical features
        # excluding targets and timestamp from input features
        X = dfm.drop(['Available_Spaces', 'Available_Bikes', 'Last_Update'], 1)
        Y = dfm[['Available_Bikes']]  # target outcome to predict

        # Generate time series cross validation splits (using default of 5 splits)
        tscv = TimeSeriesSplit()

        for train_index, test_index in tscv.split(X):
            # Generate training and test data
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]

            stations_list.append(station)

            # Generate model with training data
            multiple_linreg = LinearRegression().fit(X_train, Y_train)

            # pickle and save model
            joblib.dump(multiple_linreg, "linear_regression_model_{}.pkl".format(station))

            # Evaluate model on test data
            multiple_linreg_predictions = multiple_linreg.predict(X_test)

            # Print the metrics to judge the model's accuracy
            rmse = np.sqrt(metrics.mean_squared_error(Y_test, multiple_linreg_predictions))
            rmse_list.append(rmse)
            mae = metrics.mean_absolute_error(Y_test, multiple_linreg_predictions)
            mae_list.append(mae)
            r2 = metrics.r2_score(Y_test, multiple_linreg_predictions)
            r2_list.append(r2)

    results_d = {'Stop_Number': stations_list, 'RMSE': rmse_list, 'MAE': mae_list, 'R2': r2_list}
    results_df = pd.DataFrame(data=results_d)
    return results_df


