import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
from matplotlib import pyplot as plt

data = pd.read_csv('analog_data_2.csv')
# some_data = data.tail(400)
# some_data.plot(kind='line',
#                x='Time',
#                y='Amplitude')
# plt.show()

data['Normalized'] = np.int16((data['Amplitude'] / data['Amplitude'].max()) * 32767)
max = data['Amplitude'].max()
min = data['Amplitude'].min()
median = int((max-min)/2) + min
data['Signed'] = data['Amplitude'] - median
data['Time'] = pd.to_datetime(data['Time'])
# some_data = data.tail(400)
# some_data.plot(kind='line',
#                x='Time',
#                y='Normalized')
# plt.show()

N = len(data)
mx = data['Time'].max()
mn = data['Time'].min()
i = mx-mn
seconds = i.total_seconds()
zero_crossings = np.where(np.diff(np.sign([i for i in data['Signed'] if i])))[0]
freq = (len(zero_crossings)/seconds)/2
avg = i.total_seconds()/(N-1)
yf = fft(data['Signed'])
xf = fftfreq(N, avg)
data['frequency'] = xf
data['f_amplitude'] = np.abs(yf)
data = data.sort_values('f_amplitude', ascending=False)


input()
plt.plot(xf, np.abs(yf))
plt.show()