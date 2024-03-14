import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

print('********************Part1************************')
# RESAMPLE:
dates = pd.date_range('1/3/2024', periods=11, freq='D')
# print(dates)
time_range = np.arange(1, len(dates) + 1)
# print(time_range)
time_series = pd.Series(time_range, dates)
print("1. time series:\n", time_series)

# bucket into 3 days
time_series.resample('3D')
# print(time_series.resample('3D').first())
# print(time_series.resample('3D').last())

try:
  attempt = pd.Series(time_range).resample('W')
except TypeError:
  print("please try resample on a series with a time index")
else:
  print(attempt)

df1 = pd.DataFrame({
  'days': time_series,
  'weeks': time_series.resample('W').first()
})

# # either:
# df1 = df1.fillna(0)
# print(df1.astype({'days': 'int', 'weeks': 'int'}))
# or:
print(df1.astype('Int64'))

# OHLC:
print(time_series.resample('W').ohlc())
print(time_series.resample('W').last())

print('********************Part2************************')
tick_data_path = os.getenv("TICK_DATA")
with open(tick_data_path, 'r') as file:
  tick_data = file.read()
tick_data_df = pd.read_csv(tick_data_path, names=['date&time', 'LTP', 'LTQ', 'code'], index_col=0)
tick_data_df.index = pd.to_datetime(tick_data_df.index, format='%Y-%m-%d %H:%M:%S:%f')
print('1. tick data:\n', tick_data_df)

# resample LTP column to 1 hour bars and divide it into OHLC format
resample_LTP = tick_data_df['LTP'].resample('1h').ohlc()
print('2. resample LTP column:\n', resample_LTP)

tick_data_df = tick_data_df.astype({'LTQ': 'float'})
resample_LTQ = tick_data_df.resample('1h').agg({'LTQ':'sum'})
print('3. resample LTQ column:\n', resample_LTQ)

resample_data = pd.concat([resample_LTP, resample_LTQ], axis=1)
print("4. resample LTP and LTQ:\n", resample_data)