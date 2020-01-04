# NSE Stocks Analysis

This is an app developed to monitor the trends around top 100 stocks trading in India's National Stock Exchange(NSE). This app gives the breakdown of performance of different stocks by sector, their overall volatility in the last 52 weeks and the comparison of the stock's current price against its 52 weeks high & low. This app was built using the Dash framework in Python.

Dash abstracts away all of the technologies and protocols required to build an interactive web-based application and is a simple and effective way to bind a user interface around your Python code. 

## Running the app locally

Clone the git repo, then install the requirements with pip
```
git clone https://github.com/arpitsolanki/NSE_Stocks_Analysis
cd dash-sample-apps/apps/dash-oil-and-gas
pip install -r requirements.txt

#Run the app
python my_app1.py
```

## About the app
This Dash app displays last 52 weeks performance of top 100 stocks listed in India's National Stock Exchange. The app fetches the current and historical prices from Google Finance API. The data for this is stored in a Googlesheet at the backend where the data is stored. 

## Built With
Googlesheet Finance API - For fetching stock prices and common metrics associated with a stock
Dash - Main server and interactive components
Plotly Python - Used to create the interactive plots

## Screenshots
The following are screenshots for the app in this repo:

![Alt text](screenshots/Snip1.png)

![Alt text](screenshots/snip2.png)

![Alt text](screenshots/snip3.png)

