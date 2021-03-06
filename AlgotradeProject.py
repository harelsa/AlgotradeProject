# -*- coding: utf-8 -*-
"""Robo-Advis-Prod.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rk6rAuQ0Z1Xt_1J9SSOYIe3Vbo6g0MNq
"""
# !pip install matplotlib
# !pip install yfinance
# !pip install seaborn
# pip install numpy
# Importing all the libraries

from pandas_datareader import data as pdr

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

test_periods = [
    {"start_year": '2005-1-1', "end_year": '2008-1-1', 'predict_year': '2009-1-1'},
    {"start_year": '2005-6-1', "end_year": '2008-6-1', 'predict_year': '2009-6-1'},
    {"start_year": '2006-1-1', "end_year": '2009-1-1', 'predict_year': '2010-1-1'},
    {"start_year": '2006-6-1', "end_year": '2009-6-1', 'predict_year': '2010-6-1'},
    {"start_year": '2007-1-1', "end_year": '2010-1-1', 'predict_year': '2011-1-1'},
    {"start_year": '2007-6-1', "end_year": '2010-6-1', 'predict_year': '2011-6-1'},
    {"start_year": '2008-1-1', "end_year": '2011-1-1', 'predict_year': '2012-1-1'},
    {"start_year": '2008-6-1', "end_year": '2011-6-1', 'predict_year': '2012-6-1'},
    {"start_year": '2009-1-1', "end_year": '2012-1-1', 'predict_year': '2013-1-1'},
    {"start_year": '2009-6-1', "end_year": '2012-6-1', 'predict_year': '2013-6-1'},
    {"start_year": '2010-1-1', "end_year": '2013-1-1', 'predict_year': '2014-1-1'},
    {"start_year": '2010-6-1', "end_year": '2013-6-1', 'predict_year': '2014-6-1'},
    {"start_year": '2011-1-1', "end_year": '2014-1-1', 'predict_year': '2015-1-1'},
    {"start_year": '2011-6-1', "end_year": '2014-6-1', 'predict_year': '2015-6-1'},
    {"start_year": '2012-1-1', "end_year": '2015-1-1', 'predict_year': '2016-1-1'},
    {"start_year": '2012-6-1', "end_year": '2015-6-1', 'predict_year': '2016-6-1'},
    {"start_year": '2013-1-1', "end_year": '2016-1-1', 'predict_year': '2017-1-1'},
    {"start_year": '2013-6-1', "end_year": '2016-6-1', 'predict_year': '2017-6-1'},
    {"start_year": '2014-1-1', "end_year": '2017-1-1', 'predict_year': '2018-1-1'},
    {"start_year": '2014-6-1', "end_year": '2017-6-1', 'predict_year': '2018-6-1'},
    {"start_year": '2015-1-1', "end_year": '2018-1-1', 'predict_year': '2019-1-1'},
    {"start_year": '2015-6-1', "end_year": '2018-6-1', 'predict_year': '2019-6-1'},
    {"start_year": '2016-6-1', "end_year": '2019-6-1', 'predict_year': '2020-6-1'},
    {"start_year": '2016-1-1', "end_year": '2019-1-1', 'predict_year': '2020-1-1'}
]

periods_stocks_prices = {}
periods_portfolios = {}

for period in test_periods:
    # Select stocks, start year and end year, stock number has no known limit
    ## Insert Parmater
    selected = ["SPY", "QQQ", "IEI", "LQD", "TA35.TA", "VWO", "DJT"]  # The Name Tiker
    start_year = period['start_year']
    end_year = period['end_year']
    prediction_year = period['predict_year']
    Num_porSimulation = 50000  # Number of Portfolio that will build for simulator
    stocks_prices = {}
    ## End Insert Parameter
    # Select stocks, start year and end year, stock number has no known limit

    # Building the DataBase
    yf.pdr_override()
    frame = {}
    for stock in selected:
        data_var = pdr.get_data_yahoo(stock, start_year, end_year)['Adj Close']
        data_var.to_frame()
        frame.update({stock: data_var})
        # get the price of each stock at the end of the tested period and one year after
        predict_price = pdr.get_data_yahoo(stock, end_year, prediction_year)['Adj Close']
        stocks_prices[stock] = {'start_val': predict_price[0], 'end_val': predict_price[len(predict_price) - 1]}
    periods_stocks_prices[period['predict_year']] = stocks_prices
    # End Insert Adj Close To DataBase

    import pandas as pd

    # Mathematical calculations Return Daily And annualy, creation of Number portfolios,
    table = pd.DataFrame(frame)
    returns_daily = table.pct_change()
    returns_annual = ((1 + returns_daily.mean()) ** 250) - 1

    # get daily and covariance of returns of the stock
    cov_daily = returns_daily.cov()
    cov_annual = cov_daily * 250

    # empty lists to store returns, volatility and weights of imiginary portfolios
    port_returns = []
    port_volatility = []
    sharpe_ratio = []
    stock_weights = []

    # set the number of combinations for imaginary portfolios
    num_assets = len(selected)
    num_portfolios = Num_porSimulation  # Change porfolio numbers here

    # set random seed for reproduction's sake
    np.random.seed(101)

    # populate the empty lists with each portfolios returns,risk and weights
    for single_portfolio in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        returns = np.dot(weights, returns_annual)
        returns = np.dot(weights, returns_annual)
        # calculation the Standard Deviation of portfolio.
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
        # calculation the sharpe of portfolio.
        sharpe = returns / volatility
        sharpe_ratio.append(sharpe)
        # Percent Conversion
        port_returns.append(returns * 100)
        port_volatility.append(volatility * 100)
        stock_weights.append(weights)

    # a dictionary for Returns and Risk values of each portfolio
    portfolio = {'Returns': port_returns,
                 'Volatility': port_volatility,
                 'Sharpe Ratio': sharpe_ratio}

    # extend original dictionary to accomodate each ticker and weight in the portfolio
    for counter, symbol in enumerate(selected):
        portfolio[symbol + ' Weight'] = [Weight[counter] for Weight in stock_weights]

    # make a nice dataframe of the extended dictionary
    df = pd.DataFrame(portfolio)

    # get better labels for desired arrangement of columns
    column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in selected]

    # reorder dataframe columns
    df = df[column_order]

    # plot frontier, max sharpe & min Volatility values with a scatterplot
    # find min Volatility & max sharpe values in the dataframe (df)
    min_volatility = df['Volatility'].min()
    # min_volatility1 = df['Volatility'].min()+1
    max_sharpe = df['Sharpe Ratio'].max()
    max_return = df['Returns'].max()
    max_vol = df['Volatility'].max()
    # use the min, max values to locate and create the two special portfolios
    sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
    min_variance_port = df.loc[df['Volatility'] == min_volatility]
    max_returns = df.loc[df['Returns'] == max_return]
    max_vols = df.loc[df['Volatility'] == max_vol]

    # plot frontier, max sharpe & min Volatility values with a scatterplot
    # plt.style.use('seaborn-dark')
    # df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
    #                 cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    # plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='green', marker='D', s=200)
    # plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='orange', marker='D', s=200)
    # plt.scatter(x=max_vols['Volatility'], y=max_returns['Returns'], c='red', marker='D', s=200)
    # plt.style.use('seaborn-dark')
    #
    # plt.xlabel('Volatility (Std. Deviation) Percentage %')
    # plt.ylabel('Expected Returns Percentage %')
    # plt.title(period['send_year'])
    # plt.subplots_adjust(bottom=0.4)
    # ------------------ Pritning 3 optimal Protfolios -----------------------
    # Setting max_X, max_Y to act as relative border for window size

    red_num = df.index[df["Returns"] == max_return]
    yellow_num = df.index[df['Volatility'] == min_volatility]
    green_num = df.index[df['Sharpe Ratio'] == max_sharpe]
    multseries = pd.Series([1, 1, 1] + [100 for stock in selected],
                           index=['Returns', 'Volatility', 'Sharpe Ratio'] + [stock + ' Weight' for stock in selected])

    with pd.option_context('display.float_format', '%{:,.2f}'.format):
        # keep for each period of prediction all the three portfolios data
        periods_portfolios[period['predict_year']] = {
            'max_returns': df.loc[red_num[0]].multiply(multseries),
            'safest': df.loc[yellow_num[0]].multiply(multseries),
            'sharp': df.loc[green_num[0]].multiply(multseries)}
        # plt.figtext(0.2, 0.15, "Max returns Porfolio: \n" + df.loc[red_num[0]].multiply(multseries).to_string(),
        #             bbox=dict(facecolor='red', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center',
        #             wrap=True)
        # plt.figtext(0.45, 0.15, "Safest Portfolio: \n" + df.loc[yellow_num[0]].multiply(multseries).to_string(),
        #             bbox=dict(facecolor='yellow', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center',
        #             wrap=True)
        # plt.figtext(0.7, 0.15, "Sharpe  Portfolio: \n" + df.loc[green_num[0]].multiply(multseries).to_string(),
        #             bbox=dict(facecolor='green', alpha=0.5), fontsize=11, style='oblique', ha='center', va='center',
        #             wrap=True)

    # plt.show()
    # print(periods_stocks_prices)
    # print(periods_portfolios)

    """
    #################################################
    Testing Robo-Adviser Project 
    
    - performing analysis on a few periods and 7 different stocks 
    - finding the differences in Robo-Adviser Returns prediction for each portfolio and make an analysis of the results 
    - finding the differences in Robo-Adviser total prediction returns  for all portfolios and make an analysis 
    #################################################
    
    """

"""
    # selected_stocks-all stock names
    # returns- returns in percentage by robo.
    # portfolio_percentage- split by percentage of investment
    # real_profit_percentage- difference between end and start of stocks value
    # return the difference between Robo' Prediction and reality
"""


def returnsDiffrence(selected, portfolio, periods_stocks_prices):
    returns = portfolio["Returns"]

    real_profit = 0.0
    for stock in selected:
        real_profit = real_profit + (
                portfolio[stock + " Weight"] * periods_stocks_prices[stock]['difference'] - portfolio[
            stock + " Weight"])
    return returns - real_profit


# find the  prices diff from the beginning of a period and the end
for period in periods_stocks_prices:
    for mystock in periods_stocks_prices[period]:
        difference = 1.0 + (periods_stocks_prices[period][mystock]['end_val'] - periods_stocks_prices[period][mystock][
            'start_val']) / periods_stocks_prices[period][mystock]['start_val']
        periods_stocks_prices[period][mystock]["difference"] = difference
# init data frame of real returns diff
"""
    Period / Portfolio    |     safest   |   max_returns   |   sharp 
    
    2008-1-1 -> 20012-1-1       +0.5%            -0.7%          +7.5%   
        ...
        ...
        
"""
index = periods_stocks_prices.keys()
columns = ['max_returns', 'safest', 'sharp']
idx = pd.Index(index, name='Dates')
df_ = pd.DataFrame(index=idx, columns=columns)
df_ = df_.fillna(0.0)  # with 0s rather than NaNs

# get periods
for period_key in index:
    # key = period_key['start_year'] + '->' + period_key['end_year']
    period_info = periods_portfolios[period_key]
    for portfolio in period_info:
        row = df_.loc[period_key]
        row[portfolio] = returnsDiffrence(selected, period_info[portfolio], periods_stocks_prices[period_key])

# plt.show()


"""
#################
Results analysis 
#################
"""
# have to use abs before calc the mean and std
print(df_)
print("mean safest: " + str(df_["safest"].mean()))
print("std safest: " + str(df_["safest"].std()))

print("mean sharp: " + str(df_["sharp"].mean()))
print("std sharp: " + str(df_["sharp"].std()))

print("mean max_returns: " + str(df_["max_returns"].mean()))
print("std max_returns: " + str(df_["max_returns"].std()))

# plot analyst graph

from matplotlib import style

plt.clf()

#first graph
style.use('ggplot')
# df_.plot( y=columns, kind="line")
df_['max_returns'].plot(ls='-.')
df_['safest'].plot(ls='-')
df_['sharp'].plot(ls=':')
plt.legend(loc=4)
plt.xlabel('Test Prediction Date of the Learning Period', fontsize=14)
plt.ylabel('Percentage(%)Diff', fontsize=14)
plt.grid(axis='x', color='0.95')
plt.legend(title='Portfolio Type:')
plt.title('Returns Differences by Stock Portfolio Type', fontsize=18)
plt.show()

# mean graph

plt.clf()
df_.mean().plot(kind='bar', hatch= '/' , color='green')
plt.xlabel('Portfolio Type', fontsize=14)
plt.ylabel('Mean Percentage(%)Diff', fontsize=14)
plt.grid(axis='x', color='0.95')
plt.title('Returns Differences by Stock Portfolio Type', fontsize=18)
plt.show()

# std graph
plt.clf()
df_.std().plot(kind='bar', hatch= '+' , color='blue')
plt.xlabel('Portfolio Type', fontsize=14)
plt.ylabel('Std Percentage(%)Diff', fontsize=14)
plt.grid(axis='x', color='0.95')
plt.title('Returns Differences by Stock Portfolio Type', fontsize=18)

plt.show()
