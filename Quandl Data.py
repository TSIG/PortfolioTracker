import quandl
import time
import numpy as np
import pandas as pd


#ticker = "AAPL"
#buy_date = "2016-9-24"
#current_date = time.strftime("%Y/%m/%d")
#current_date = time.strftime("%Y/%m?%d")


#pandas_DF = quandl.get("WIKI/AAPL",start_date = buy_date, end_date = current_date)

#print(pandas_DF['Open'])

class Stock:
    def __init__(self, ticker, buy_date):
        #init details of stock
        self.ticker = 'WIKI/' + ticker
        self.buy_date = buy_date
        self.percent_change = 0
        #grab stock's info since buy date
        self.pandas_DF = quandl.get(self.ticker, start_date = self.buy_date, end_date = time.strftime("%Y/%m?%d"))
                
        
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