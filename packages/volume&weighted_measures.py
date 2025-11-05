import pandas as pd
import numpy as np
import yfinance as yf


def calculate_vmw(ticker, interval, vwm, period_ma):

    if interval in ['1m', '2m', '5m', '15m', '30m']:
        period = '7d'

    if interval in ['1h', '90']:
        period = '60d'

    if interval in ['1d', '1wk', '1mo', '3mo']:
        period = 'max'

    #==================ADD DATA FETCHING HERE==================

    data = yf.download(ticker, period=period, interval=interval)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]

    #==========================================================

    # ALL VMWS

    if vwm == 'obv':
        obv = [0]
        for i in range(1, len(data)):
            if data['close'].iloc[i] > data['close'].iloc[i-1]:
                obv.append(obv[-1] + data['volume'].iloc[i])

            elif data['close'].iloc[i] < data['close'].iloc[i-1]:
                obv.append(obv[-1] - data['volume'].iloc[i])

            else:
                obv.append(obv[-1])

        data['vwm'] = obv

        if not period_ma:
            period_ma = 20

        data['vwm_ma'] = data['obv'].rolling(period_ma).mean()
        

    elif vwm == 'vwap':
        typical_price = (data['high'] + data['low'] + data['close'])/3
        data['vwm'] = (typical_price * data['volume']).cumsum() / data['volume']


    elif vwm == 'cmf':
        if not period_ma:
            period_ma = 20

        mf_multiplier = ((data['close'] - data['low']) - (data['high'] - data['close'])) / (data['high'] - data['low'])
        mf_volume = mf_multiplier* data['volume']
        data['vwm'] = mf_volume.rolling(period_ma).sum() / data['volume'].rolling(period_ma).sum()

    elif vwm == 'adl':
        mf_multiplier = ((data['close'] - data['low']) - (data['high'] - data['close'])) / (data['high'] - data['low'])
        mf_volume = mf_multiplier * data['volume']
        data['vwm'] = mf_volume.cumsum()



    days = data.index.strftime("%Y-%m-%d %H:%M:%S").tolist()
    if 'vwm' not in data:
        data['vwm'] = np.nan
    if 'vwm_ma' not in data:
        data['vwm_ma'] = np.nan
    

    return {
        'labels': days,
        'vwm': data['vwm'].astype(float).replace({np.nan:None}).tolist(),
        'vwm_ma': data['vwm_ma'].astype(float).replace({np.nan:None}).tolist()
    }




    


    



    






