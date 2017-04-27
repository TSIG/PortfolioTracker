# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pyodbc
import quandl
import time
import pandas as pd
from datetime import datetime, timedelta
import datetime


class Stock:
    def __init__(self, ticker, buy_date):
        #init details of stock
        self.ticker = ticker
        self.DBticker = 'WIKI/' + ticker
        self.buy_date = buy_date
        self.percent_change = 0
        #grab stock's info since buy date
        self.pandas_DF = quandl.get(self.DBticker, start_date = self.buy_date, end_date = time.strftime("%Y/%m?%d"))
	#add date column
        self.pandas_DF['Date'] = pd.to_datetime(self.pandas_DF.index)
                
    def display_5_day(self):
        DF_5_day = self.pandas_DF.iloc[::5, :]
        return DF_5_day
               
    #function displays the start pricings of each month 
    def display_1_month(self):
        #sort by asencding date order
        DF_1_month = self.pandas_DF.sort_index()
        #retain only the beginning month prices
        return DF_1_month.groupby(pd.TimeGrouper('M')).nth(0)
        
        
    def display_3_month(self):
        DF_3_month = self.pandas_DF.sort_index()
        DF_3_month = DF_3_month.groupby(pd.TimeGrouper('M')).nth(0)
        #retain every 3rd month
        return DF_3_month.iloc[::3, :]
        
    def display_1_year(self):
        DF_1_year = self.pandas_DF.sort_index()
        #retain every year
        return DF_1_year.groupby(pd.TimeGrouper('12M')).nth(0)
        
        
    def display_total(self):
        return self.pandas_DF
    
    def get_ticker(self):
        return self.ticker
    
    #function for getting previous day's stock information. Need to add parameters for weekend vs weekday
    def get_day_update(self):
        DF_1_day = quandl.get(self.DBticker, start_date = datetime.date.today()
        - timedelta(days=1), end_date = datetime.date.today() - timedelta(days=1))
        return DF_1_day


ticker = 'AAPL'
test = Stock(ticker, "2016-10-24")


server = 'cs1'
db1 = 'TSIG-StockDatabase'
tcon = 'yes'
uname = 'nrode17'
pword = '6336523NdR'

    
q = '''\
insert into PortfolioStockList
    ( 
        CompanyTicker, 
        Date, 
        PriceOpen, 
        PriceHigh, 
        PriceLow, 
        PriceClose, 
        Volume, 
        ExDividend, 
        SplitRatio, 
        AdjOpen, 
        AdjHigh, 
        AdjLow, 
        AdjClose, 
        AdjVolume)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
connection = pyodbc.connect(driver='{SQL Server};',
                            host = server,
                            database = db1,
                            trusted_connection=tcon, user=uname, password=pword)
cursor = connection.cursor()


for index, row in test.display_total().iterrows():
    cursor.execute(q, test.get_ticker(), row['Date'], row['Open'], row['High'], row['Low'],
    row['Close'], row['Volume'], row['Ex-Dividend'], row['Split Ratio'], 
    row['Adj. Open'], row['Adj. High'], row['Adj. Low'], row['Adj. Close'], row['Adj. Volume'])
    
#connection.commit()
connection.close()
print("END")
