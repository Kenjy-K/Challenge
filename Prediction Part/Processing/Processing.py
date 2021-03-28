#%%
#Packages
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from math import ceil
#%%
#Get the data
df = pd.read_excel("Time Series Bike.xlsx")
# %%
# to explicitly convert the date column to type DATETIME
df['Date'] = pd.to_datetime(df['Date'])
df.dtypes
# %%
#Plot
x = df["Date"]
y = df["Total"]

plt.plot(x,y)
plt.xlabel("Date")
plt.ylabel("Nombre de passages de vélos")
plt.title("Nombre de passages journaliers de vélos au point de comptage Albert 1er")

df.head()
# %%
#Change into a time series
indexedDataset = df.set_index('Date')
indexedDataset.sort_index(inplace=True)
indexedDataset.index
indexedDataset.plot()
# %%
# Estimating trend : log
indexedDataset_logScale = np.log(indexedDataset)
plt.plot(indexedDataset_logScale)

# %%
# Get the difference between the moving average and the actual number of passengers
datasetLogScaleMinusMovingAverage = indexedDataset_logScale - movingAverage
datasetLogScaleMinusMovingAverage.head(12)
#Remove Nan Values
datasetLogScaleMinusMovingAverage.dropna(inplace=True)
datasetLogScaleMinusMovingAverage.head(10)
# %%

def test_stationarity(timeseries):
    
    #Determing rolling statistics
    movingAverage = timeseries.rolling(window=12).mean()
    movingSTD = timeseries.rolling(window=12).std()

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(movingAverage, color='red', label='Rolling Mean')
    std = plt.plot(movingSTD, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries['Total'], autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

#%%
test_stationarity(indexedDataset_logScale)
test_stationarity(indexedDataset)

# %%
#Decomposition tend, seasonal, residual
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(indexedDataset_logScale, period = 30)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(indexedDataset_logScale, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal,label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
# %%
import statsmodels.api as sm 
fig = plt.figure(figsize=(12,4))
#Raw log plots
ax1 = fig.add_subplot(221)
fig = sm.graphics.tsa.plot_acf(indexedDataset_logScale, lags=24, ax=ax1)
ax2 = fig.add_subplot(222)
fig = sm.graphics.tsa.plot_pacf(indexedDataset_logScale, lags=24, ax=ax2)
#%%
# Automatic ARIMA coeff determination 
# Ignore harmless warnings
from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")
  
# Fit auto_arima function to AirPassengers dataset
stepwise_fit = auto_arima(indexedDataset_logScale['Total'], start_p = 1, start_q = 1,
                          max_p = 3, max_q = 3, m = 12,
                          start_P = 0, seasonal = True,
                          d = None, D = 1, trace = True,
                          error_action ='ignore',   # we don't want to know if an order does not work
                          suppress_warnings = True,  # we don't want convergence warnings
                          stepwise = True)           # set to stepwise
  
# To print the summary
stepwise_fit.summary()

#%%
from statsmodels.tsa.statespace.sarimax import SARIMAX
(p,d,q) = (0,1,1)

#creatin of the model with determined coeff
mod = SARIMAX(indexedDataset_logScale, order = (p,d,q), seasonal_order = (p,d,q, 12))
res = mod.fit()

import datetime
from dateutil.relativedelta import *

#We set date list
date_list = pd.date_range(start = max(indexedDataset_logScale.index), end = '2021-04-02 00:00:00')
future = pd.DataFrame(index=pd.to_datetime(date_list), columns=['Total'])
pred_df = pd.concat([pd.DataFrame(indexedDataset_logScale), future])

#Exponential data
pred_log = res.predict(start = 0, end = len(pred_df))
pred = np.exp(pred_log)
print("Le nombre de vélos prévus pour le 02/04/2021 est de:", ceil(pred.iloc[-1]))

# Prediction
prediction = pred.iloc[-1] *0.12
print("Le nombre de vélos prévus pour le 02/04/2021, entre 00:00 et 09:00 est de:", ceil(prediction))

# %%
