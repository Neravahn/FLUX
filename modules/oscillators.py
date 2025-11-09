import yfinance as yf
import pandas as pd
import numpy as np

def oscillator_calculate(ticker, interval, oscillator, period, fast, slow, signal):


    # FETCHING DATA FOR OSCILLATORS 
    if interval in ['1m', '2m', '5m', '15m', '30m']:
        period_df = '7d'

    elif interval in ['1h', '90m']:
        period_df = '60d'

    elif interval in ['1d', '1wk', '1mo', '3mo']:
        period_df = 'max'


    data = yf.download(ticker, period=period_df , interval=interval)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]

    try:
        # OSCILLATORS [ FOR OSCILLATORS NOT HAVING SIGNAL IMMA EXPLICITLY ADD IT AND SET TO NONE]
        if oscillator == 'rsi':
            if not period:
                period = 14

            delta = data['close'].diff()
            gain = delta.clip(lower = 0)
            loss = -delta.clip(upper = 0)
            avg_gain = gain.ewm(alpha=1/period, adjust = False).mean()
            avg_loss = loss.ewm(alpha = 1/period, adjust= False).mean()
            rs = avg_gain / avg_loss
            data['oscillator'] = 100 - (100/(1 + rs))
            data['oscillator_signal'] = None


        elif oscillator == 'macd':
            if not fast:
                fast = 12

            if not slow:
                slow = 26

            if not signal:
                signal = 9

            
            ema_fast = data['close'].ewm(span = fast, adjust=False).mean()
            ema_slow = data['close'].ewm(span = slow, adjust = False).mean()

            data['macd'] = ema_fast - ema_slow
            data['signal'] = data['macd'].ewm(span = signal, adjust=False).mean()
            data['hist'] = data['macd'] - data['signal']
            data['oscillator'] = data['macd']
            data['oscillator_signal'] = data['signal']


        elif oscillator == 'william_r':
            if not period:
                period = 14

            high_max = data['high'].rolling(period).max()
            low_min = data['low'].rolling(period).min()
            data['oscillator'] = -100 * (high_max - data['close'])/ (high_max - low_min)
            data['oscillator_signal'] = None


        elif oscillator == 'stochastic':
            if not period:
                period = 14

            low_min = data['low'].rolling(period).min()
            high_max = data['high'].rolling(period).max()

            data['%k'] = (data['close'] - low_min) / (high_max - low_min)*100
            data['%d'] = data['%k'].rolling(3).mean()

            data['oscillator'] = data['%k']
            data['oscillator_signal'] = data['%d']


        elif oscillator == 'momentum':
            if not period:
                period = 10

            data['oscillator'] = data['close'] - data['close'].shift(period)
            data['oscillator_signal'] = None


        elif oscillator == 'roc':
            if not period:
                period = 12

            data['oscillator'] = (data['close'] / data['close'].shift(period) -1 )* 100
            data['oscillator_signal'] = None


        elif oscillator == 'trix':
            if not period:
                period = 15

            ema_1 = data['close'].ewm(span = period, adjust = False).mean()
            ema_2 = ema_1.ewm(span = period, adjust = False).mean()
            ema_3 = ema_2.ewm(span = period, adjust = False).mean()

            data['oscillator'] = ema_3.pct_change() * 100
            data['oscillator_signal'] = None


        elif oscillator == 'cci':
            if not period:
                period = 20

            tp = (data['high'] + data['low'] + data['close']) / 3
            sma = tp.rolling(period).mean()
            mad = (tp - sma).abs().rolling(period).mean()
            data['oscillator'] = (tp - sma) / (0.05 * mad)
            data['oscillator_signal'] = None


        elif oscillator == 'mfi':
            if not period:
                period = 14
            
            tp = (data['high'] + data['low'] + data['close']) / 3
            mf = tp * data['volume']
            pos = pd.Series(np.where (tp> tp.shift(1), mf, 0), index =tp.index)
            neg = pd.Series(np.where (tp < tp.shift(1), mf, 0), index=tp.index)
            pos_sum = pos.rolling(period).sum()
            neg_sum = neg.rolling(period).sum()
            mfr = pos_sum / neg_sum
            data['oscillator'] = 100 - (100 / (1 + mfr))
            data['oscillator_signal'] = None


        elif oscillator == 'tsi':
            r = 25
            s = 13

            diff = data['close'].diff()
            abs_diff = diff.abs()
            ema_1 = diff.ewm(span=r, adjust = False).mean()
            ema_2 = ema_1.ewm(span=2, adjust = False).mean()
            abs_ema_1 = abs_diff.ewm(span=r, adjust=False).mean()
            abs_ema_2 = abs_ema_1.ewm(span=s, adjust = False).mean()

            data['oscillator'] = 100 * (ema_2 / abs_ema_2)
            data['oscillator_signal'] = None



        days = data.index.strftime("%Y-%m-%d %H:%M:%S").tolist()
        if 'oscillator' not in data:
            data['oscillator'] = np.nan
        if 'oscillator_signal' not in data:
            data['oscillator_signal'] = np.nan
        if 'close' not in data:
            data['close'] = np.nan




        return {
            'labels' : days,
            'close' : data['close'].astype(float).replace({np.nan:None}).tolist(),
            'oscillator': data['oscillator'].astype(float).replace({np.nan:None}).tolist(),
            "oscillator_signal": data['oscillator_signal'].astype(float).replace({np.nan:None}).tolist()
        }

    except Exception as e:
        return {'error' : str(e)}


