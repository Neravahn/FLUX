import numpy as np
import yfinance as yf
import pandas as pd



def calculate_gbm(ticker, interval, th_gbm, nos_gbm, drift_gbm, volatility_gbm):
    


    if interval in ['1m', '2m', '5m', '15m', '30m']:
        period = '7d'


    elif interval in ['1h', '90m']:
        period = '60d'


    elif interval in ['1d', '1wk', '1mo', '3mo']:
        period = '1y'


    else:
        period = '5y'


    data = yf.download(ticker, period = period, interval=interval, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]
    prices = data['close']


    try:
        #   CALCULATING DRIFT AND VOLATILITY
        if not drift_gbm :
            returns = prices.pct_change().dropna()
            mu = returns.mean()
        else:
            mu = int(drift_gbm)



        if not volatility_gbm:
            returns = prices.pct_change().dropna()
            sigma = returns.std()
        else:
            sigma = int(volatility_gbm)



        if not th_gbm:
            th_gbm = 30
        else:
            th_gbm = int(th_gbm)



        if not nos_gbm:
            nos_gbm = 10
        else:
            nos_gbm = int(nos_gbm)
            



        if sigma == 0 or np.isnan(sigma):
            sigma = 1e-6




        #SIMULATE GBM PATHS
        price0 = prices.iloc[-1]

        dt =1.0

        simulations = np.zeros((nos_gbm, th_gbm))
        dt = 1/th_gbm

        for i in range(nos_gbm):
            path = np.zeros(th_gbm)
            path[0] = price0
            for t in range(1, th_gbm):
                epsilon = np.random.normal()
                path[t] = path[t-1] * np.exp((mu-0.5 * sigma**2)*dt + sigma *np.sqrt(dt) *epsilon)
            simulations[i, :] = path
        

        result = {
            'simulations':  simulations.tolist(),
            'labels': list(range(th_gbm))
        }

        return result

    except Exception as e:
        return {'error': str(e)}


