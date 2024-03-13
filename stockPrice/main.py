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