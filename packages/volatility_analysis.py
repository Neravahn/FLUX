import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import math

def volatility_analysis(df):
    df = df.sort_index()
    
    train = df['close'][:int(len(df)*0.9)]
    test = df['close'][int(len(df)*0.9):]

    try:
        model = ARIMA(train, order=(1, 1, 1))
        model_fit = model.fit()

        predictions = model_fit.forecast(steps=len(test)) # here arima will be predicting usin regression analysis 

        #now we will check the predicted vs actual data and calculate mea and rmse 

        mae = mean_absolute_error(test, predictions)
        rmse = math.sqrt(mean_squared_error(test, predictions))

        if rmse > test.mean() * 0.07: #i have set 7% as the volatility threshold
            interpretation = "HIGHLY VOLATILE"

        elif 0.05< rmse < 0.07:
            interpretation = " MODERATELY VOLATILE"
        else:
            interpretation = "LOW VOLATILE"

        return{
            "MAE": mae,
            "RMSE" : rmse,
            "Interpretation" : interpretation
        }
    except Exception as e:
        return {"Error": str(e)}





