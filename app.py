from datetime import datetime, timedelta
from flask import Flask, render_template, request
import json
import matplotlib
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
app = Flask(__name__)
matplotlib.use('Agg')

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


def one_investment_strategy(data, amount, strategy):
    allStockPortfolio = []
    currentInvestmentAmount = 0
    investmentAmount = int(amount)
    requiredInfo = []
    for stockItem in data[strategy]:
        info = []
        stockPortfolio = []
        investedAmount = (int(stockItem['percentage']) / 100) * investmentAmount
        stock = yf.Ticker(stockItem['symbol'])
        if strategy == 'Index Investing':
            currentStockPrice = stock.info['navPrice']
        else:
            currentStockPrice = stock.info['currentPrice']
        info.append(stockItem['name'])
        info.append(investedAmount)
        info.append(currentStockPrice)
        requiredInfo.append(info)
        stock = yf.Ticker(stockItem['symbol'])
        hist = stock.history(period="5d")
        numberShares = investedAmount / currentStockPrice
        for price in hist['Close']:
            stockPortfolio.append(price * numberShares)
        allStockPortfolio.append(stockPortfolio)
        currentInvestmentAmount += (currentStockPrice * numberShares)

    totalPortfolio = []
    for ind in range(len(allStockPortfolio[0])):
        s = 0
        s = s + allStockPortfolio[0][ind] + allStockPortfolio[1][ind] + \
            allStockPortfolio[2][ind] + allStockPortfolio[3][ind]
        totalPortfolio.append(s)

    currentTime = datetime.now()
    currentDay = currentTime.strftime('%m-%d-%Y')
    d = str(currentDay)
    d1 = datetime.strptime(d, '%m-%d-%Y')
    dates = [(d1-timedelta(days=i)).strftime('%m-%d-%Y')
             for i in range(5, 0, -1)]
    plt.clf()
    plt.plot(dates, totalPortfolio)
    plt.xlabel("Last 5 days")
    plt.ylabel("Amount (USD)")
    plt.title("Weekly Portfolio Trend")
    plt.savefig('static/images/investment-strategy.jpeg')
    pie_one_investment = np.array([])
    pie_labels = []
    for stockItem in data[strategy]:
        pie_one_investment = np.append(pie_one_investment, int(stockItem['percentage']))
        pie_labels.append(stockItem['name'])
    plt.clf()
    plt.title("Distribution of money for each stock")
    plt.pie(pie_one_investment, labels = pie_labels)
    plt.savefig('static/images/pie_chart-investment-strategy.jpeg')
    return requiredInfo

def two_investment_strategy(data, amount, strategy1, strategy2):
    allStockPortfolio = []
    currentInvestmentAmount = 0
    investmentAmount = int(int(amount) / 2)
    requiredInfo = []
    for stockItem in data[strategy1]:
        info = []
        stockPortfolio = []
        investedAmount = (int(stockItem['percentage']) / 100) * investmentAmount
        stock = yf.Ticker(stockItem['symbol'])
        if strategy1 == 'Index Investing':
            currentStockPrice = stock.info['navPrice']
        else:
            currentStockPrice = stock.info['currentPrice']
        info.append(stockItem['name'])
        info.append(investedAmount)
        info.append(currentStockPrice)
        requiredInfo.append(info)
        stock = yf.Ticker(stockItem['symbol'])
        hist = stock.history(period="5d")
        numberShares = investedAmount / currentStockPrice
        for price in hist['Close']:
            stockPortfolio.append(price * numberShares)
        allStockPortfolio.append(stockPortfolio)
        currentInvestmentAmount += (currentStockPrice * numberShares)
    for stockItem in data[strategy2]:
        info = []
        stockPortfolio = []
        investedAmount = (int(stockItem['percentage']) / 100) * investmentAmount
        stock = yf.Ticker(stockItem['symbol'])
        if strategy2 == 'Index Investing':
            currentStockPrice = stock.info['navPrice']
        else:
            currentStockPrice = stock.info['currentPrice']
        info.append(stockItem['name'])
        info.append(investedAmount)
        info.append(currentStockPrice)
        requiredInfo.append(info)
        stock = yf.Ticker(stockItem['symbol'])
        hist = stock.history(period="5d")
        numberShares = investedAmount / currentStockPrice
        for price in hist['Close']:
            stockPortfolio.append(price * numberShares)
        allStockPortfolio.append(stockPortfolio)
        currentInvestmentAmount += (currentStockPrice * numberShares)

    totalPortfolio = []
    for ind in range(len(allStockPortfolio[0])):
        s = 0
        s = s + allStockPortfolio[0][ind] + allStockPortfolio[1][ind] + \
            allStockPortfolio[2][ind] + allStockPortfolio[3][ind] + allStockPortfolio[4][ind] + allStockPortfolio[5][ind] + allStockPortfolio[6][ind] + allStockPortfolio[7][ind]
        totalPortfolio.append(s)

    currentTime = datetime.now()
    currentDay = currentTime.strftime('%m-%d-%Y')
    d = str(currentDay)
    d1 = datetime.strptime(d, '%m-%d-%Y')
    dates = [(d1-timedelta(days=i)).strftime('%m-%d-%Y')
             for i in range(5, 0, -1)]

    plt.clf()
    plt.plot(dates, totalPortfolio)
    plt.xlabel("Last 5 days")
    plt.ylabel("Amount (USD)")
    plt.title("Weekly Portfolio Trend")
    plt.savefig('static/images/two_investment-strategy.jpeg')
    pie_two_investment = np.array([])
    pie_labels = []
    for stockItem in data[strategy1]:
        pie_two_investment = np.append(pie_two_investment, int(stockItem['percentage'])/2)
        pie_labels.append(stockItem['name'])
    for stockItem in data[strategy2]:
        pie_two_investment = np.append(pie_two_investment, int(stockItem['percentage'])/2)
        pie_labels.append(stockItem['name'])
    plt.clf()
    plt.title("Distribution of money for each stock")
    plt.pie(pie_two_investment, labels = pie_labels)
    plt.savefig('static/images/pie_chart-two-investment-strategy.jpeg')
    return requiredInfo


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    name = output["name"]
    strategy = output["strategy"]
    with open('investing_strategies.json') as f:
        data = json.load(f)

    l = strategy.split()

    if len(strategy.split()) == 2:
        info = one_investment_strategy(data, name, strategy)
        stock1 = info[0][0]
        stock2 = info[1][0]
        stock3 = info[2][0]
        stock4 = info[3][0]
        stock1_price = info[0][2]
        stock2_price = info[1][2]
        stock3_price = info[2][2]
        stock4_price = info[3][2]
        stock1_money = info[0][1]
        stock2_money= info[1][1]
        stock3_money = info[2][1]
        stock4_money = info[3][1]
        return render_template('one_strategy.html', name = name, strategy = strategy, stock1 = stock1, stock2 = stock2, stock3 = stock3,
                               stock4 = stock4, stock1_price = stock1_price, stock2_price = stock2_price, stock3_price = stock3_price,
                               stock4_price = stock4_price, stock1_money = stock1_money, stock2_money = stock2_money, stock3_money = stock3_money,
                               stock4_money = stock4_money, url = 'static/images/investment-strategy.jpeg', url_pie = 'static/images/pie_chart-investment-strategy.jpeg')
    else:
        amount = int(name)
        strategy1_list = l[0:2]
        strategy2_list = l[3:]
        strategy1 = ' '.join(strategy1_list)
        strategy2 = ' '.join(strategy2_list)
        info = two_investment_strategy(data, amount, strategy1, strategy2)
        stock1 = info[0][0]
        stock2 = info[1][0]
        stock3 = info[2][0]
        stock4 = info[3][0]
        stock1_price = info[0][2]
        stock2_price = info[1][2]
        stock3_price = info[2][2]
        stock4_price = info[3][2]
        stock1_money = info[0][1]
        stock2_money = info[1][1]
        stock3_money = info[2][1]
        stock4_money = info[3][1]
        stock5 = info[4][0]
        stock6 = info[5][0]
        stock7 = info[6][0]
        stock8 = info[7][0]
        stock5_price = info[4][2]
        stock6_price = info[5][2]
        stock7_price = info[6][2]
        stock8_price = info[7][2]
        stock5_money = info[4][1]
        stock6_money = info[5][1]
        stock7_money = info[6][1]
        stock8_money = info[7][1]
        return render_template('two_strategies.html', name = name, strategy1 = strategy1, strategy2 = strategy2, stock1 = stock1, stock2 = stock2,
                               stock3 = stock3, stock4 = stock4, stock5 = stock5, stock6 = stock6, stock7 = stock7, stock8 = stock8,
                               stock1_price = stock1_price, stock2_price = stock2_price, stock3_price = stock3_price, stock4_price = stock4_price,
                               stock5_price = stock5_price, stock6_price = stock6_price, stock7_price = stock7_price, stock8_price = stock8_price,
                               stock1_money = stock1_money, stock2_money = stock2_money, stock3_money = stock3_money, stock4_money = stock4_money,
                               stock5_money = stock5_money, stock6_money = stock6_money, stock7_money = stock7_money, stock8_money = stock8_money,
                               url = 'static/images/two_investment-strategy.jpeg', url_pie = 'static/images/pie_chart-two-investment-strategy.jpeg')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
