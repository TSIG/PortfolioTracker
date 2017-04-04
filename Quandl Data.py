import quandl
import time


ticker = "AAPL"
buy_date = "2016-9-24"
current_date = time.strftime("%Y/%m/%d")



pandas_DF = quandl.get("WIKI/AAPL",start_date = buy_date, end_date = current_date)

print(pandas_DF['Open'])


