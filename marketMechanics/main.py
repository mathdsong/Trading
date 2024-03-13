import numpy as np
import pandas as pd

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


