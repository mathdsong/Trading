import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

stock_price_path = os.getenv("STOCK_PRICE")

with open(stock_price_path, 'r') as file:
  stock_price = file.read()

# generate a DataFrame from csv file with fields and some calculations:
stock_price_df = pd.read_csv(stock_price_path, names=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close', 'adj_volume'])
print("1. overall data:")
print(stock_price_df)
print("2. the median for each field regardless ticker:")
print(stock_price_df.median(numeric_only=True))
print("3. the median of each field for each ticker:")
stock_price_df_ticker_groups = stock_price_df.groupby('ticker')
print(stock_price_df_ticker_groups.median(numeric_only=True))
# create a pivot table which reshape the dataframe such that for each field, we can easily see the stock price on different days:
pivot_table = stock_price_df.pivot(index='date', columns='ticker', values=['open', 'high', 'low', 'close', 'volume', 'adj_close', 'adj_volume'])
print("4. overall pivot table:")
print(pivot_table)
print("5. the median value of each field for each ticker:")
print(pivot_table.median(numeric_only=True))
# create open-price pivot table:
open_price_pivot_table = stock_price_df.pivot(index='date', columns='ticker', values='open')
print("6. open-price pivot table:")
print(open_price_pivot_table)
# transpose the open-price pivot table:
transpose_open_pivot = open_price_pivot_table.T
print("7. transpose of open-price pivot table:")
print(transpose_open_pivot)
print("8. the mean value for each date: ")
print(transpose_open_pivot.mean(numeric_only=True))

def csv_to_close_price(csv_filepath, field_names) :
    """Reads in data from a csv file and produces a DataFrame with close data.

    Parameters
    ----------
    csv_filepath : str
         Thename of the csv file to read
    field_names : list of str
        The field names of the field in the csv file

    Returns
    -------
    close : DataFrame
        Close prices for each ticker and date
    """
    # read the csv file into the dataframe:
    df = pd.read_csv(csv_filepath, names=field_names)
    # generate the close-price pivot table:
    close_price_pivot_table = df.pivot(index='date', columns='ticker', values='close')
    return close_price_pivot_table

print(csv_to_close_price(stock_price_path, ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close', 'adj_volume']))

def pivot_ohlc_price(keyWord, csv_filepath, field_names) :
    # read the csv file into the dataframe:
    df = pd.read_csv(csv_filepath, names=field_names)
    df['date'] = pd.to_datetime(df['date'])
    # generate the close-price pivot table:
    pivot_table = df.pivot(index='date', columns='ticker', values=keyWord)
    return pivot_table

def days_to_weeks(open_prices, high_prices, low_prices, close_prices):
    """Converts daily OHLC prices to weekly OHLC prices.

    Parameters
    ----------
    open_prices : DataFrame
        Daily open prices for each ticker and date
    high_prices : DataFrame
        Daily high prices for each ticker and date
    low_prices : DataFrame
        Daily low prices for each ticker and date
    close_prices : DataFrame
        Daily close prices for each ticker and date

    Returns
    -------
    open_prices_weekly : DataFrame
        Weekly open prices for each ticker and date
    high_prices_weekly : DataFrame
        Weekly high prices for each ticker and date
    low_prices_weekly : DataFrame
        Weekly low prices for each ticker and date
    close_prices_weekly : DataFrame
        Weekly close prices for each ticker and date
    """

    open_prices_weekly = open_prices.resample('W').first()
    high_prices_weekly = high_prices.resample('W').max()
    low_prices_weekly = low_prices.resample('W').min()
    close_prices_weekly = close_prices.resample('W').last()

    return open_prices_weekly, high_prices_weekly, low_prices_weekly, close_prices_weekly

ohlc_list = ['open', 'high', 'low', 'close']
pd_list = []
for i in ohlc_list:
    pivot_table = pivot_ohlc_price(i, stock_price_path, ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close', 'adj_volume'])
    pd_list.append(pivot_table)

# print(pd_list[0].resample('W').first())
# print(pd_list[1].resample('W').max())
# print(pd_list[2].resample('W').min())
# print(pd_list[3].resample('W').last())
print(days_to_weeks(pd_list[0], pd_list[1], pd_list[2], pd_list[3]))