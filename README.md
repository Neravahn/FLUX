FLUX

FLUX is an interactive Python web application for exploring stock prices, technical indicators, and market trends. It combines real-time data with interactive charts to provide a clean and user-friendly analysis experience.

🚀 Features

Real-time stock data: Fetch historical and intraday stock prices via Yahoo Finance.

Technical indicators: OBV, VWAP, CMF, ADL, moving averages.

Interactive charts: Zoom, pan, toggle grid, tooltips.

Customizable analysis: Select tickers, benchmarks, intervals, and indicator periods.

Download charts: Export visualizations as PNG images.


💻 Installation
# Clone repository
git clone https://github.com/Neravahn/FLUX.git
cd FLUX

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py


Open your browser at:

http://127.0.0.1:5000

🛠 Usage

Enter a stock ticker and benchmark symbol.

Choose a time interval (e.g., 1d, 1h, 5m).

Select a technical indicator (OBV, VWAP, CMF, ADL).

Click Submit to generate interactive charts.

Use Reset Zoom and Toggle Grid for customized visualization.

Click Download Chart to save the chart as PNG.

📊 Supported Indicators
Indicator	Description
OBV	On-Balance Volume: tracks cumulative buying/selling pressure
VWAP	Volume Weighted Average Price: measures average trading price
CMF	Chaikin Money Flow: identifies accumulation/distribution trends
ADL	Accumulation/Distribution Line: shows money inflow/outflow
MA	Moving Average: smooths indicator trends
🧰 Technologies

Python 3 – backend logic

Flask – web framework

yfinance – stock data retrieval

Pandas & NumPy – data manipulation

Chart.js – interactive charts

HTML/CSS/JavaScript – frontend
