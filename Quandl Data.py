# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import pyodbc
import quandl
import time
import pandas as pd
from datetime import datetime, timedelta
import datetime


class SQLConnection:
    def __init__(self):
        self.server = 'cs1'
        self.db1 = 'TSIG-StockDatabase'
        self.tcon = 'yes'
        self.uname = 'nrode17'
        self.pword = '6336523NdR'
        self.connection = pyodbc.connect(driver='{SQL Server};', 
                                            host = self.server, 
                                            database = self.db1, 
                                            trusted_connection=self.tcon, 
                                            user=self.uname, 
                                            password=self.pword)                     
        self.cursor = self.connection.cursor()
        
        
        
        
        #Query for storing the Portfolio stock data
        self.storePortfolioDataQuery = '''\
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
        
        #Query that creates a temp table that will store data that the user
        #searches for, not portfolio stock data
        self.createTempTableQuery = '''\
        create table #TempPortfolio
            (
                CompanyTicker nchar(5) not null, 
                Date date, 
                PriceOpen float, 
                PriceHigh float, 
                PriceLow float, 
                PriceClose float, 
                Volume int, 
                ExDividend float, 
                SplitRatio float, 
                AdjOpen float, 
                AdjHigh float, 
                AdjLow float, 
                AdjClose float, 
                AdjVolume int)
        '''
        
        
        #Query that inserts the temporary stock data into the temp table
        self.insertIntoTempTableQuery = '''\
        insert into #TempPortfolio
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
        
        #actually executes the query for creating the table
        self.cursor.execute(self.createTempTableQuery)

    #Executes putting the portfolio data into the db    
    def execute_insertPortfolioData(self, stock):
        for index, row in stock.display_total().iterrows():
            self.cursor.execute(self.storePortfolioDataQuery, stock.get_ticker(), row['Date'], row['Open'],
            row['High'], row['Low'], row['Close'], row['Volume'], 
            row['Ex-Dividend'], row['Split Ratio'], row['Adj. Open'],
            row['Adj. High'], row['Adj. Low'], row['Adj. Close'], 
            row['Adj. Volume'])
            
            
   #Commits and closes the connection and queries         
    def commit_and_close(self):
        self.connection.commit()
        self.connection.close()



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
print(test.get_day_update())

newSQL = SQLConnection()
newSQL.execute_insertPortfolioData(test)
newSQL.commit_and_close()

print("END")
