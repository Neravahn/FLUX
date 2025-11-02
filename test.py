import pandas as pd
import numpy as np
import yfinance as yf

def rolling_mean(x, n):
    return x.rolling(int(n)).mean()

def run_formula(formula):
    data = yf.download("AAPL", period="1mo")
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]
    env = {
        'close': data['close'],
        'rolling_mean': rolling_mean,
        'sqrt': np.sqrt
    }
    try:
        data['custom'] = eval(formula, {"__builtins__": {}}, env)
        data['custom'] = data['custom'].replace({np.nan: None})
        return data[['close','custom']].head(10)
    except Exception as e:
        return str(e)

print(run_formula("rolling_mean(close, 5)"))

