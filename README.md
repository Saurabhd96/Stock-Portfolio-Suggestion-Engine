# Stock-Portfolio-Suggestion-Engine

User will enter amount to invest in USD (Minimum is $5000 USD). The Stock Portfolio Suggestion Engine will recommend a set of stocks, return the current value of the stock, show the money distribution for buying the stocks and return the overall portfolio trend over the last 5 days. yfinance api is used to get information related to the stocks.

## Steps to run the application
  - Ensure that Python (version 3.6 or 3.7) and pip are installed in the system.
  - Ensure that there is a strong internet connection as the application needs yfinance api to get information about stocks.
  - pip3 install --upgrade --no-cache-dir -r requirements.txt
  - python3 -m flask run
  - Navigate to http://127.0.0.1:5000/
