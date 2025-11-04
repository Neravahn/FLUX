from flask import Flask, render_template, url_for, request, jsonify
import yfinance as yf
from packages.volatility_analysis import volatility_analysis
from packages.return_analysis import return_analysis
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from packages.beta_alpha import calculate_beta_alpha
from packages.risk_return_analysis import calculate_risk_return
from packages.quant_core import run_formula
import traceback
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/analyse', methods=['GET','POST'])
def analyse():
    if request.method == 'POST':
        ticker = request.form["ticker"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        analysis_type = request.form["analysis_type"]

        df = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(1)
        df.columns = [col.lower() for col in df.columns]

        if df.empty:
            return 'no data available for this date range'
        
        if analysis_type == "volatility":
            result = volatility_analysis(df)
            return render_template("vol_result.html", result = result, ticker = ticker)
        
        
        elif analysis_type == "returns":
            result = return_analysis(df)
            return render_template("return_result.html", result = result, ticker = ticker)
    
        else:
            return "Analysis type invalid"



@app.route('/correlation')
def correlation():
    return render_template('correlation.html')

@app.route('/correlation_analysis', methods = ['POST'])
def correlation_analysis():

    data = request.get_json()
    ticker_1 = data['ticker_1']
    ticker_2 = data['ticker_2']
    start_date = data['start_date']
    end_date = data['end_date']

    df_1 = yf.download(ticker_1, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)
    if isinstance(df_1.columns, pd.MultiIndex):
        df_1.columns = df_1.columns.get_level_values(1)
    df_1.columns = [col.lower() for col in df_1.columns]

    df_2 = yf.download(ticker_2, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)
    if isinstance(df_2.columns, pd.MultiIndex):
        df_2.columns = df_2.columns.get_level_values(1)
    df_2.columns = [col.lower() for col in df_2.columns]

    df = pd.DataFrame({
        'ticker1': df_1['close'].pct_change(),
        'ticker2': df_2['close'].pct_change()
        }).dropna()
    
    corr = df['ticker1'].corr(df['ticker2'])

    if corr > 0.7:
        interpretation = "Highly positively correlated — move together strongly."
    elif corr > 0.3:
        interpretation = "Moderately correlated — move in same direction most times."
    elif corr > -0.3:
        interpretation = "Weak or no correlation — move independently."
    else:
        interpretation = "Negatively correlated — often move opposite."

    points = df.reset_index().apply(lambda row:{
        'x' : round(row['ticker1']* 100, 3),
        'y': round(row['ticker2']* 100, 2)
    }, axis = 1).tolist()

    return jsonify({
        'points': points,
        'corr': round(corr, 3),
        'interpretation': interpretation
    })


@app.route('/moving_average')
def moving_average():
    return render_template('moving_average.html')

@app.route('/m_a_analysis', methods = ['GET', 'POST'])
def m_a_analysis():
    if request.method == 'POST':
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        moving_average_type = request.form['moving_average_type']
        window = int(request.form.get('window'))

        df = yf.download(ticker, start=start_date, end=end_date, group_by='ticker', auto_adjust=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(1)
        df.columns = [col.lower() for col in df.columns]

        if df.empty:
            return 'no data available for this date'
        
        if moving_average_type == 'sma':
            df['ma'] = df['close'].rolling(window = window).mean()
            label = f'SMA {{window}}'

        elif moving_average_type == 'wma':
            weights = np.arange(1, window+1)
            df['ma']= df['close'].rolling(window).apply(lambda prices: np.dot(prices, weights)/ weights.sum(), raw= True)
            label = f'WMA {{window}}'

        elif moving_average_type == 'cma':
            df['ma'] = df['close'].expanding().mean()
            label = f'CMA {{window}}'

        elif moving_average_type == 'ema':
            df['ma'] = df['close'].ewm(span=window, adjust=False.mean())
            label = f'EMA {{window}}'
        
        elif moving_average_type == 'hma':
            half = max(1, int(window/2))
            sqrt = max(1, int(np.sqrt(window)))
            wma_half = df['close'].rolling(half).mean()
            wma_full = df['close'].rolling(window).mean()
            df['ma'] = ((2 * wma_half) - wma_full).rolling(sqrt).mean()
            label = f'WMA {{window}}'

        elif moving_average_type == 'tma':
            sma = df['close'].rolling(window).mean()
            df['ma'] = sma.rolling(window).mean()

        else:
            return jsonify({'error': "unknown moving average type"})

    df2 = df[['close', 'ma']].dropna()
    if df2.empty:
        return jsonify({'error': 'not enough data'})
    
    result = {
        'index' : [d.strftime('%y-%m-%d')for d in df.index],
        'close': df['close'].round(6).tolist(),
        'ma': df2['ma'].round(6).tolist(),
        'ticker': ticker
    }

    return jsonify(result)

        
@app.route('/risk_return_summary')
def risk_return_summary():
    return render_template('risk_return_main.html')

@app.route('/rr_analysis', methods = ['GET', 'POST'])
def rr_analysis():
    if request.method == 'POST':
        ticker = request.form['ticker']
        benchmark = request.form['benchmark']
        start_date = request.form['start_date']
        end_date =request.form['end_date']
        frequency = request.form['frequency']

        result = calculate_risk_return(ticker, benchmark, start_date, end_date, frequency)

    return render_template('rr_result.html', result = result)

















@app.route('/flux_engine')
def flux_engine():
    return render_template('flux_engine.html')

@app.route('/engine', methods=['POST'])
def engine():

    data = request.get_json()
    try:
        ticker = data['ticker']
        interval = data['interval']
        formula_1 = data['formula_1']
        formula_2 = data['formula_2']
        moving_average = data['moving_average']
        window = data['window']

        result = run_formula(ticker, interval, formula_1, formula_2, moving_average, window)
        # print("RETURNING TO FRONTEND:", result)
        print("Returned keys:", result.keys())



        
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/alphabeta_engine', methods = ['POST'])
def alphabeta_engine():
    data = request.get_json()
    try:
        ticker = data['ticker_alphabeta']
        benchmark = data['benchmark']
        interval = data['interval']

        result = calculate_beta_alpha(ticker, benchmark, interval)

        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

    




  


if __name__ == '__main__':
    app.run(debug=True)