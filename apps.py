from flask import Flask, render_template, url_for, request, jsonify
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from packages.beta_alpha import calculate_beta_alpha
from packages.quant_core import run_formula
import traceback
import numpy as np
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

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


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

    




  


if __name__ == '__main__':
    app.run(debug=True)