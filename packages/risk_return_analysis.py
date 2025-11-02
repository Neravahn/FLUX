import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io , base64

def calculate_risk_return(ticker, benchmark, start_date, end_date,frequency):

    # FETCHING DATA
    data = yf.download(ticker, start = start_date, end = end_date)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    data.columns = [col.lower() for col in data.columns]

    data = data['close']
    bench = None
    if benchmark:
        bench = yf.download(benchmark, start = start_date, end= end_date)
        if isinstance(bench.columns, pd.MultiIndex):
            bench.columns = bench.columns.get_level_values(0)
        bench.columns = [col.lower() for col in bench.columns]

        bench = bench['close']

    df = pd.DataFrame({'price':data})
    if bench is not None:
        df['benchmark'] = bench

    df = df.resample(frequency).last()


    # COMPUTE RETURNS
    df['return'] = df['price'].pct_change().dropna()
    if benchmark:
        df['bench_ret'] = df['benchmark'].pct_change().dropna()


    mean_return = df['return'].mean()
    volatility = df['return'].std()
    annual_factor = {'D': 252, 'W':52, 'M' : 12}[frequency]
    annual_return = (1 + mean_return)**annual_factor -1
    ann_vol = volatility *np.sqrt(annual_factor)

    sharpe = annual_return / ann_vol if ann_vol != 0 else np.nan


    # MAX DRAWDOWN
    cum_returns = (1 + df['return']).cumprod()
    rolling_max = cum_returns.cummax()
    drawdown = (cum_returns - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    alpha = np.nan
    beta = np.nan
    corr = np.nan

    
    # ALPH BETA IF BENCHMARK EXISTS
    if benchmark:
        valid = df[['return', 'bench_ret']].dropna()
        cov = np.cov(valid['return'], valid['bench_ret'])[0][1]
        var_bench = np.var(valid['bench_ret'])
        beta = cov / var_bench
        alpha  = mean_return - beta * valid['bench_ret'].mean()
        corr = valid['return'].corr(valid['bench_ret'])


    # BUILT RESULT DICTIONARY
    result = {
        'ticker' : ticker,
        'benchmark': benchmark if benchmark else None,
        'annualized_return': round(annual_return*100, 2),
        'annualized_volatility': round(ann_vol*100, 2),
        'sharpe_ratio' :  round(sharpe, 2),
        'max_drawdown' : round(max_drawdown*100, 2),
        'alpha' : round(alpha*100, 2) if benchmark else None,
        'beta' : round(beta*100, 2) if benchmark else None,
        'correlation': round(corr, 2) if benchmark else None

    }


    # GENERATING CHART IF REQUESTED

    plt.figure(figsize=(10, 5))
    plt.plot(cum_returns, label=f'{ticker} cumulative returns', color = 'cyan')
    if benchmark:
        bench_cum = (1 + df['bench_ret']).cumprod()
        plt.plot(bench_cum, label=f'{benchmark} cumulative returns', color = 'orange')
    plt.title(f'cumulative return comparison({ticker})')
    plt.legend()
    plt.grid(True)

    # CREATING IMAGE
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches = 'tight')
    buffer.seek(0)
    result['charts'] = base64.b64encode(buffer.read()).decode('utf-8')
    
    plt.close()

    return result



     
