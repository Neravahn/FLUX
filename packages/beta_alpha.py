import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io , base64
from sklearn.linear_model import LinearRegression


def calculate_beta_alpha(ticker, benchmark, start_date, end_date, intervals='1d'):
    stock_df = yf.download(ticker, start= start_date, end = end_date, interval=intervals)
    bench_df = yf.download(benchmark, start = start_date, end = end_date, interval=intervals)

    for df in [stock_df, bench_df]:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns = [col.lower() for col in df.columns]
        

    
    # if isinstance(bench_df.columns, pd.MultiIndex):
    #     bench_df.columns = bench_df.columns.get_level_values(1)
    # bench_df.columns = [col.lower() for col in bench_df.columns]

    if stock_df.empty or bench_df.empty :
        return None, None
    
    
    stock_df['return'] = stock_df['close'].pct_change()

    bench_df['return'] = bench_df['close'].pct_change()

            

    merged = pd.merge(
        stock_df['return'], bench_df['return'], 
        left_index =True, right_index= True, how = 'inner'
    )
    merged.columns = ['stock_return', 'bench_return']

    merged = merged.dropna()

    if merged.empty:
        return None, None ,'not enough overlapping'
    
    x = merged['bench_return'].values.reshape(-1, 1)
    y = merged['stock_return'].values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(x, y)

    beta = model.coef_[0][0]
    alpha =model.intercept_[0]

    y_prediction = model.predict(x)

    plt.figure(figsize=(8, 5))
    plt.scatter(merged['bench_return'], merged['stock_return'],color='skyblue')
    plt.plot(merged['bench_return'], y_prediction,color='red', label = 'regression line')
    plt.title(f'Beta-Alpha analysis {ticker} vs {benchmark}')
    plt.xlabel(f'{benchmark} return')
    plt.ylabel(f'{ticker} return')
    plt.legend()
    plt.grid(True, alpha = 0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches ='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    if beta>1:
        interpretation = f'{ticker} is **more volatile** than the benchmark {benchmark}'
    elif beta<1:
        interpretation = f'{ticker} is **less volatile** than the benchmark {benchmark}'
    else:
        interpretation = f'{ticker} **moves in line** with benchmatk {benchmark}'

    if alpha > 0:
        performance = f"Positive alpha -> {ticker} **outperformed** the benchmark after adjusting for risk"

    else:
        performance = f'Negative alph -> {ticker} **underperformed** the benchmark after adjusting for risk'

    return round(alpha, 5), round(beta, 3),performance,  interpretation, image_base64