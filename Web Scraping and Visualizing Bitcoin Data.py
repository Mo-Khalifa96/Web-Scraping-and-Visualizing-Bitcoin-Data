#Web Scraping and Visualizing Bitcoin Data Using PyCoinGecko 


#Importing the Python modules to use 
import pandas as pd
from pycoingecko import CoinGeckoAPI
import plotly.graph_objects as go


#Part One: Web scraping Bitcoin prices
#In this part I will use Python's pycoingecko module to extract Bitcoin prices from CoinGecko. 
#I will specify the range of time to examine the prices across as 90 days. After extracting the 
#Bitcoin data, I'll organize it into a dataframe, clean up the data, and render it more reader-friendly.

#First, creating a CoinGecko object
cg = CoinGeckoAPI()

#Extracting BitCoin prices (in USD) for the last 90 days
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin',   #specifying type of cryptocurrency as Bitcoin
                    vs_currency='usd',    #specifying the prices in terms of USD
                    days=90)           #specifying the range of time (90 days)

#To extract the 'prices' coloumn only (consists of dates and prices)
bitcoin_prices = bitcoin_data['prices']     

#Now converting data extracted into dataframe comprised of the timestamps and prices
df_bitcoin = pd.DataFrame(bitcoin_prices, columns=['TimeStamp', 'Price'])

#previewing the dataframe (first 5 enteries)
print(df_bitcoin.head())
print('')

#Cleaning up the data
#i. Converting timestamps into reader-friendly dates
dates_col = pd.to_datetime(df_bitcoin['TimeStamp'], unit='ms')
df_bitcoin.insert(loc=0, column='Date', value=dates_col)       #inserting the adjusted dates into the dataframe

#deleting unnecessary 'TimeStamp' coloumn
del df_bitcoin['TimeStamp']

#previewing the dataframe again 
print(df_bitcoin.head())
print('')

#ii. Converting the prices into reader-friendly USD prices
df_bitcoin_in_USD = df_bitcoin.copy()
df_bitcoin_in_USD['Price'] = df_bitcoin_in_USD['Price'].apply(lambda price: '${:,.2f}'.format(price))

#changing the dates to make them day first (instead of year first)
df_bitcoin_in_USD['Date'] = df_bitcoin_in_USD['Date'].dt.strftime('%d/%m/%y %H:%M')

#Finally, reporting the results
print(df_bitcoin_in_USD)
print('')


#Part Two: Plotting the Bitcoin prices using a candlestick chart
#Now that the data were scraped and cleaned up, I'll use the plotly library to plot the data using
#a candlestick chart. But first, to create the candlesticks, I'll have to extract from the necessary 
#price data for the candlesticks, including the opening price, high price, low price, and closing price. 


#First, extracting the days of the month from the Date coloumn to group the data by day  
days_month_col = pd.to_datetime(df_bitcoin['Date']).dt.strftime('%d/%m')
df_bitcoin.insert(loc=2, column='Days of Month', value=days_month_col)              #inserting days_month_col into the dataframe


#Grouping the data by day and creating appropriate price categories for creating the candlesticks
candlestick_data = df_bitcoin.groupby(['Days of Month'], sort=False).agg({'Price': ['first', 'max', 'min', 'last']})      #calculating the price categories 

#to preview the resulting table 
print(candlestick_data.head())
print('')

#Now extracting price categories for the candlesticks 
open_price = candlestick_data['Price']['first']
high_price = candlestick_data['Price']['max']
low_price = candlestick_data['Price']['min']
close_price = candlestick_data['Price']['last']


#Creating the candlestick chart
#Specifying the x-axis data (days of month)
DaysOfMonth = candlestick_data.index.values 


#Finally using plotly to create the candlestick chart 
fig = go.Figure(data=[go.Candlestick(x=DaysOfMonth,
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price)])


#adding a title
fig.update_layout(title='Bitcoin Prices Chart')
#adding labels to the axes
fig.update_xaxes(title_text="Date")
fig.update_yaxes(title_text="Bitcoin Price (in USD)")

#To display the chart 
fig.show()


#END