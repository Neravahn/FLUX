import pandas as pd
import numpy as np
import yfinance as yf
from scipy.stats import norm


def calculate_vnr(ticker, vnr, interval, period_ma, confidence, risk_free ):
    if period_ma:
        period_ma = int(period_ma)


    if interval in ['1m', '2m', '5m', '15m', '30m']:
        period = '7d'

    elif interval in ['1h', '90m']:
        period = '60d'

    else:
        period = 'max'


    data = yf.download(ticker, period=period, interval=interval)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]


    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors = 'coerce')

    data['return'] = np.log(data['close'] / data['close'].shift(1))
    data['return'] = pd.to_numeric(data['return'], errors='coerce')



    try:
        if vnr == 'bollinger':
            if not period_ma:
                period_ma = 10

            data['ma'] = data['close'].rolling(period_ma).mean()
            data['std'] = data['close'].rolling(period_ma).std()
            data['upper'] = data['ma'] + 2 * data['std']
            data['lower'] = data['ma'] -2 * data['std']
            data['vnr'] = data['ma']



        elif vnr == 'atr':
            if not period_ma:
                period_ma = 14

            high_low = data['high'] - data['low']
            high_close = np.abs(data['high'] - data['close'].shift(1))
            low_close = np.abs(data['low'] - data['close'].shift(1))
            tr = np.maximum.reduce([high_low, high_close, low_close])
            data['vnr'] = pd.Series(tr).rolling(period_ma).mean()


        elif vnr == 'variance':
            if not period_ma:
                period_ma = 30 

            data['vnr'] = data['return'].rolling(period_ma).var()


        elif vnr == 'sharpe':
            if not risk_free:
                risk_free = 0.5
            epsilon = 1e-9
            mean_return = data['return'].mean() * 252
            std_return = data['return'].std()*np.sqrt(252)
            data['vnr'] = (mean_return - risk_free) / (std_return + epsilon)


        elif vnr == 'sortino':
            if not risk_free:
                risk_free = 0.5

            return_clean = data['return'].dropna().astype(float)

            if len(return_clean) == 0:
                data['vnr'] = np.nan

            else:
                mean_return = return_clean.mean() * 252
                downside_std = return_clean[return_clean < 0].std() * np.sqrt(252)
                epsilon = 1e-9
                vnr_value =( mean_return - risk_free) / (downside_std + epsilon)
                

            data['vnr'] =  np.full(len(data), vnr_value, dtype=float)


        elif vnr == 'var':
            if not confidence:
                confidence = 0.95

            mu = data['return'].mean()
            sigma = data['return'].std()
            data['vnr'] = mu + norm.ppf(1 - confidence) * sigma



        days = data.index.strftime("%Y-%m-%d %H:%M:%S").tolist()
        if 'vnr' not in data:
            data['vnr'] = None

        if 'lower' not in data:
            data['lower'] = None

        if 'upper' not in data:
            data['upper'] = None



        return {
            'labels': days,
            'vnr' : data['vnr'].astype(float).replace({np.nan:None}).tolist(),
            'lower': data['lower'].astype(float).replace({np.nan:None}).tolist(),
            'upper': data['upper'].astype(float).replace({np.nan:None}).tolist()

        }

    except Exception as e:
        return {'error': str(e)}



        

