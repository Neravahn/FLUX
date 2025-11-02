import pandas as pd


def return_analysis(df):
    daily_return = df['close'].pct_change().dropna()
    cum_return = (1 + daily_return).prod() - 1
    avg_daily_return = daily_return.mean()
    annualized_return = (1 + avg_daily_return) ** 252 - 1

    if cum_return > 0.5 :
        interpretation = "EXCELLENT GROWTH"
    elif 0.2 <cum_return<=0.5:
        interpretation = "MODERATE GROWTH"
    elif -0.1 <= cum_return <= 0.2:
        interpretation = "STABLE / NEUTRAL"
    elif -0.3 <= cum_return <= -0.1:
        interpretation = "DECLINING"
    else:
        interpretation = "HEAVY LOSS"
    return {
        "cum_return": round(cum_return * 100, 2), 
        "annualized_return": round(annualized_return *100, 2),
        "Interpretation": interpretation

    }
    