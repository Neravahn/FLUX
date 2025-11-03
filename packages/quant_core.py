import pandas as pd
import yfinance as yf
import numpy as np


def run_formula(ticker, interval, formula_1, formula_2, moving_average, window):

    """
    I  am making this module so that user can create their own custom moving averages without coding.
    They will have to enter only a one liner formula and using this module they can create their own 
    moving average. I have used all numpy functions which can be used on both series and number
    to make a simple and understandable function which a non coder can also understand

    Added more custom functions like rsi, zscore etc to make it more useful and also added prebuilt moving averages

    I will make it more robust but adding error handling and also more funtions so that user can create comple formulas
    easily.

    """

    # FETCH DATA FOR ALL THE FUNCTIONS OF THE TERMINAL
    if interval in ['1m', '2m', '5m', '15m', '30m']:

        period = '7d' 
    
    elif interval in['1h', '90m']:
        period = '60d'

    elif interval in ['1d', '1wk', '1mo', '3mo']:
        period = 'max'

    
    data = yf.download(ticker, period = period, interval=interval)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]




#=========================================================
# CREATING ENVIORMENT FOR SAFELY PARSING THE FORMULA
#=========================================================


    # ALLOWED VARIABLES , FUNCTIONS and ROLLING WINDOW

    allowed_var = {
        'price' : data['close'],
        'close' : data['close'],
        'high' : data['high'],
        'low' : data['low'],
        'open' : data['open'],
        'volume' : data['volume']

    }


    # ALLOWED FUNCTIONS

    allowed_fun = {

        'abs': np.abs, 'sqrt': np.sqrt, 'power': np.power, 'exp': np.exp,
        'log': np.log, 'log10': np.log10, 'sign': np.sign, 'round': np.round,
        'floor': np.floor, 'ceil': np.ceil, 'clip': np.clip, 'mod': np.mod,
        'mean': np.mean, 'median': np.median, 'std': np.std, 'var': np.var,
        'min': np.min, 'max': np.max, 'sum': np.sum, 'prod': np.prod,
        'percentile': np.percentile, 'quantile': np.quantile,
         'nanmean': np.nanmean, 'nanstd': np.nanstd,
        'where': np.where, 'maximum': np.maximum, 'minimum': np.minimum,
        'isfinite': np.isfinite, 'isnan': np.isnan, 'all': np.all, 'any': np.any,
        'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
        'arcsin': np.arcsin, 'arccos': np.arccos, 'arctan': np.arctan,
        'degrees': np.degrees, 'radians': np.radians,
        'sinh': np.sinh, 'cosh': np.cosh, 'tanh': np.tanh,
        'diff': lambda x, n=1: pd.Series(np.diff(x, n, prepend=np.nan), index=x.index),
        'cumsum': lambda x: pd.Series(np.cumsum(x), index=x.index),
        'cumprod': lambda x: pd.Series(np.cumprod(x), index=x.index)

    }

    # ALLOWED PREDEFINED FUNCTIONS

    def rolling_mean(x , rw):
        return x.rolling(int(rw)).mean()
    

    def rolling_std(x, rw):
        return x.rolling(int(rw)).std()
    

    def rolling_sum(x, rw):
        return x.rolling(int(rw)).sum()


    def rsi(x, rw):
        delta = x.diff()
        gain = delta.where(delta > 0,0)
        loss = -delta.where(delta<0, 0)
        avg_gain = gain.rolling(int(rw)).mean()
        avg_loss = loss.rolling(int(rw)).mean()
        rs= avg_gain/avg_loss
        return 100 - ( 100 / ( 1 + rs))


    def zscore(x , rw):
        a = x.rolling(int(rw)).mean()
        b = x.rolling(int(rw)).std()
        return (x - a) / b


    def sma(x, rw):
        return x.rolling(int(rw)).mean()


    def ema(x, rw):
        return x.ewm(int(rw) , adjust=False).mean()


    def wma(x, rw):
        weights = np.arange(1, int(rw) + 1)
        return x.rolling(int(rw)).apply(lambda prices: np.dot(prices,weights)/weights.sum(), raw=True)


    def vwap(price, volume):
        return (price*volume).cumsum()/volume.cumsum()


    def momentum(x, period):
        return x - x.shift(int(period))
    

    def roc(series, period):
        return (series /series.shift(period) - 1) * 100
    

    def cumulative_return(series):
        return ( 1 + series.pct_change()).cumprod() - 1
    
    
    def rolling_volatility(x , rw):
        return x.pct_change().rolling(int(rw)).std() * np.sqrt(rw)


        



    # ADDING IN ENVIORMENT
    env =  {**allowed_var, **allowed_fun, 
            'rolling_mean' : rolling_mean, 
            'rolling_std' : rolling_std, 
            'rolling_sum' : rolling_sum,
            'ema' :ema,
            'rsi' : rsi,
            'zscore' : zscore,
            'sma' : sma,
            'wma':wma,
            'vwap':vwap,
            'momentum':momentum,
            'roc':roc,
            "cumulative_return":cumulative_return,
            "rolling_volatility": rolling_volatility
            }




    # FORMULA PARSING 
    formula_1 = formula_1.strip()
    data['custom_1'] = eval(formula_1,  {"__builtins__": {}}, env) if formula_1 else data['close']

    formula_2 = formula_2.strip()
    data['custom_2'] = eval(formula_2,  {"__builtins__": {}}, env) if formula_2 else data['close']


    days = data.index.strftime("%Y-%m-%d %H:%M:%S").tolist()




#=========================================================
# ADDING PREBUILT MOVING AVERAGE IF REQUESTED
#=========================================================  

    window = int(window) if window else 10


    if moving_average == 'sma':
        data['ma'] = data['close'].rolling(window).mean()

    elif moving_average == 'ema':
        data['ma'] = data['close'.ewm(window, adjust=False).mean()]

    elif moving_average == 'wma':
        weights = np.arange(1, window + 1)
        data['ma'] = data['close'].rolling(window).apply(lambda prices:np.dot(prices, weights)/ weights.sum(), raw=True)

    # elif moving_average == 'vwap':
    #     data['ma'] = (data['close'] * data['volume']).cumsum() / data['volume'].cumsum()

    elif moving_average == 'tma':
        sma = data['close'].rolling(window).mean()

    elif moving_average == 'hma':
        half = max(1, int(window/2))
        sqrt = max(1, int(np.sqrt(window)))
        wma_half = data['close'].rolling(half).mean()
        wma_full = data['close'].rolling(window).mean()
        data['ma'] = ((2* wma_half) - wma_full).rolling(sqrt).mean()

    elif moving_average == 'cma':
        data['ma'] = data['close'].expanding().mean()










    return   {
        'labels': days,
        'value_1': data['custom_1'].astype(float).replace({np.nan: None}).tolist(),
        'value_2': data['custom_2'].astype(float).replace({np.nan: None}).tolist(),
        'ma_type' : data['high'].astype(float).replace({np.nan:None}).tolist(),
        'low' : data['low'].astype(float).replace({np.nan:None}).tolist(),
        'open' : data['open'].astype(float).replace({np.nan:None}).tolist(),
        'close' : data['close'].astype(float).replace({np.nan: None}).tolist()
    }
