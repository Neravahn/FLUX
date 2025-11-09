import numpy as np
import pandas as pd
import yfinance as yf



def calculate_rw(ticker, interval, th_rw, nos_rw, drift_rw, volatility_rw):
    if interval in ['1m', '2m', '5m', '15m', '30m']:
        period = '7d'

    elif interval in ['1h', '90m']:
        period = '60d'


    elif interval in ['1d', '1wk', '1mo', '3mo']:
        period = '1y'


    else:
        period = '5y'


    data = yf.download(ticker, period = period, interval = interval, progress=False)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]

    try:
        data['return'] = data['close'].pct_change().dropna()


        if not drift_rw:
            mu = data['return'].mean()
        else:
            mu = int(drift_rw)


        if not volatility_rw:
            sigma = data['return'].std()
        else:
            sigma = int(volatility_rw)

        if not nos_rw:
            nos_rw = 10
        else:
            nos_rw = int(nos_rw)

        if not th_rw:
            th_rw = 30
        else:
            th_rw = int(th_rw)


        if sigma == 0 or np.isnan(sigma):
            sigma = 1e-6


        #ACTUAL FORMULA STARTS HERE

        price0 = data['close'].iloc[-1]

        simulations = np.zeros((nos_rw, th_rw))


        
        for i in range(nos_rw):
            path = np.zeros(th_rw)
            path[0] = price0
            for t in range(1, th_rw):
                epsilon = np.random.normal()
                path[t] = path[t-1] * (1 + mu + sigma * epsilon)
            simulations[i, :] = path

        result = {
            'simulations': simulations.tolist(),
            'labels': list(range(th_rw))
        }

        return result
    except Exception as e:
        return {'error':str(e)}
