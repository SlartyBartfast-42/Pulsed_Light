import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
from matplotlib import pyplot as plt

file_name = 'Photodiode_20Hz.csv'

data = pd.read_csv(file_name)
# Backfill missing data.  Data that wasn't abel to be converted to an integer was replaced with None.
# There was typically a significant time lag associated with None values.  Data should be inspected.
# data['Amplitude'] = np.int16(data['Amplitude'].fillna(method='backfill'))

# Visually inspect the first 400 data points
some_data = data.head(400)
some_data.plot(kind='line',
               x='Time',
               y='Amplitude')

# Visually inspect the last 400 data points
some_data = data.tail(400)
some_data.plot(kind='line',
               x='Time',
               y='Amplitude')
plt.show()

# Shift the data to oscillate around 0.  Allows for 0 crossing detection algorithm
max = data['Amplitude'].max()
min = data['Amplitude'].min()
median = int((max-min)/2) + min
data['Signed'] = data['Amplitude'] - median

# Total number of data points
N = len(data)

data['Time'] = pd.to_datetime(data['Time'])
# Calculate duration of data collection
mx = data['Time'].max()
mn = data['Time'].min()
seconds = mx-mn
seconds = seconds.total_seconds()
# Use 0 crossing algorithm calculate frequency
zero_crossings = np.where(np.diff(np.sign([i for i in data['Signed'] if i])))[0]
freq = (len(zero_crossings)/seconds)/2

# Calculate seconds per reading
avg = seconds/(N-1)

# pass data to scipy fft, fftfreq
yf = fft(data['Signed'])
xf = fftfreq(N, avg)

# create sorted_data dataframe for easy comparison to results of 0 crossing algorithm
data['frequency'] = xf
data['f_amplitude'] = np.abs(yf)
sorted_data = data.sort_values('f_amplitude', ascending=False)

# graph the frequency/amplitude data
plt.plot(xf, np.abs(yf))
plt.show()

input()