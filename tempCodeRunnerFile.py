
@app.route('/flux_engine')
def flux_engine():
    return render_template('flux_engine.html')

@app.route('/engine', methods = ['GET', 'POST'])
@app.route('/engine', methods=['POST'])
def engine():
    try:
        ticker = request.form['ticker']
        interval = request.form['interval']
        formula_1 = request.form['formula_1']
        formula_2 = request.form['formula_2']

        result = run_formula(ticker, interval, formula_1, formula_2)
        
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)})

  