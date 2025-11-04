import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io , base64
from sklearn.linear_model import LinearRegression


def calculate_beta_alpha(ticker, benchmark, interval):
    if interval in ['1m', '2m', '5m', '15m', '30m']:
        period = '7d'

    elif interval in ['1h', '90m']:
        period = '60d'

    elif interval in ['1d', '1wk', '1mo', '3mo']:
        period = 'max'

    if not interval:
        period = '1d'

    stock_df = yf.download(ticker, period = period, interval = interval)
    if isinstance(stock_df.columns, pd.MultiIndex):
        stock_df.columns = stock_df.columns.get_level_values(0)
    stock_df.columns = [col.lower() for col in stock_df.columns]


    bench_df = yf.download(benchmark, period= period, interval = interval)
    if isinstance(bench_df.columns, pd.MultiIndex):
        bench_df.columns = bench_df.columns.get_level_values(0)
    bench_df.columns = [col.lower() for col in bench_df.columns]


    

    if stock_df.empty or bench_df.empty :
        return {'error' : 'No data available for the selected stock/benchmark pair'}
    
    
    stock_df['return'] = stock_df['close'].pct_change()

    bench_df['return'] = bench_df['close'].pct_change()

            

    merged = pd.merge(
        stock_df['return'], bench_df['return'], 
        left_index =True, right_index= True, how = 'inner'
    )
    merged.columns = ['stock_return', 'bench_return']

    merged = merged.dropna()

    if merged.empty:
        return {'error' : 'Not enough overlapping data points'}
    
    x = merged['bench_return'].values.reshape(-1, 1)
    y = merged['stock_return'].values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, y)

    beta = model.coef_[0][0]
    alpha =model.intercept_[0]

    y_prediction = model.predict(x)

    #CREATING DATA FOR CHART.JS

    actual_points = [
        {'x': float(b), 'y':float(s)}
        for b, s in zip(merged['bench_return'], merged['stock_return'])
    ]

    regression_line = [
        {'x': float(b), 'y': float(p)}
        for b, p in zip(merged['bench_return'], y_prediction.flatten())
    ]

    result = {
        'alpha': float(alpha),
        'beta': float(beta),
        "actual_points": actual_points,
        'regression_line': regression_line
    }


    return result


