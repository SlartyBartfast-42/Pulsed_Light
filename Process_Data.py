import pandas as pd
import numpy as np
from scipy.fft import fft, fftfreq
from matplotlib import pyplot as plt

data = pd.read_csv('analog-data.csv')
# some_data = data.tail(400)
# some_data.plot(kind='line',
#                x='Time',
#                y='Amplitude')
# plt.show()

data['Normalized'] = np.int16((data['Amplitude'] / data['Amplitude'].max()) * 32767)
data['Time'] = pd.to_datetime(data['Time'])
# some_data = data.tail(400)
# some_data.plot(kind='line',
#                x='Time',
#                y='Normalized')
# plt.show()

N = len(data)
mx = max(data['Time'])
mn = min(data['Time'])
i = mx-mn
avg = i.total_seconds()/(N-1)
yf = fft(data['Normalized'])
xf = fftfreq(N, avg)

plt.plot(xf, np.abs(yf))
plt.show()

