import pandas as pd
import yfinance as yf
import numpy as np


def run_formula(ticker, start_date, end_date, formula):

    """
    I  am making this module so that user can create their own custom moving averages without coding.
    They will have to enter only a one liner formula and using this module they can create their own 
    moving average. I have used all numpy functions which can be used on both series and number
    to make a simple and understandable function which a non coder can also understand

    Next I will add some custom functions as well like moving averages and other things

    """

    # FETCH DATA
    data = yf.download(ticker, start = start_date, end = end_date)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]




    # ALLOWED VARIABLES , FUNCTIONS and ROLLING WINDOW
    allowed_var = {
        'price' : data['close'],
        'close' : data['close'],
        'high' : data['high'],
        'low' : data['low'],
        'open' : data['open'],
        'volume' : data['volume']

    }

    

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

    # DEFINING ROLLING WINDOW CUZ LAMBA FUNCTION WAS NOT WORKING FINE
    def rolling_mean(x , rw):
        return x.rolling(int(rw)).mean()
    
    def rolling_std(x, rw):
        return x.rolling(int(rw)).std()
    
    def rolling_sum(x, rw):
        return x.rolling(int(rw)).sum()

    allowed_rolling = {
        'rolling_mean' : rolling_mean,
        'rolling_std' : rolling_std,
        'rolling_sum' : rolling_sum

    }

    env =  {**allowed_var, **allowed_fun, 
            'rolling_mean' : rolling_mean, 
            'rolling_std' : rolling_std, 
            'rolling_sum' : rolling_sum,
            }


    # FORMULA PARSING 
    formula = formula.strip()
    data['custom'] = eval(formula,  {"__builtins__": {}}, env)


    days = list(range(1, len(data) + 1))

    return   {
        'days': days,
        'values': data['custom'].astype(float).replace({np.nan: None}).tolist(),
        'close' : data['close'].astype(float).replace({np.nan: None}).tolist()
    }

    

