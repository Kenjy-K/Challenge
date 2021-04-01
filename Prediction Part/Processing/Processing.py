#%%
#Import of packages
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime
from dateutil.relativedelta import *
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from math import ceil
from pmdarima.arima import auto_arima
import warnings
warnings.filterwarnings("ignore")
#%%
# Get the data
df = pd.read_excel("Time Series Bike.xlsx")
# %%
# to explicitly convert the date column to type DATETIME
df['Date'] = pd.to_datetime(df['Date'])
df.dtypes
# %%
# Plot 
x = df["Date"]
y = df["Total"]

plt.plot(x,y)
plt.xlabel("Date")
plt.ylabel("Nombre de passages de vélos")
plt.title("Nombre de passages journaliers de vélos au point de comptage Albert 1er")

df.head()
# %%
#Change into a time series
indexed_df = df.set_index('Date')
indexed_df.sort_index(inplace=True)
indexed_df.index
indexed_df.plot()
# %%
# Estimating trend : log
log_df = np.log(indexed_df)
plt.plot(log_df)

# %%

#Definition of a function to identify if the time series is stationary or not
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
# Apply our function to dataset
test_stationarity(df)
test_stationarity(log_df)

# %%
# Decomposition tend, seasonal, residual
from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(log_df, period = 30)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(log_df, label='Original')
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
#Plot autocorrelation and partial autocorrelation graphs.
import statsmodels.api as sm 
fig = plt.figure(figsize=(12,4))

#Raw log plots
ax1 = fig.add_subplot(221)
fig = sm.graphics.tsa.plot_acf(log_df, lags=24, ax=ax1)
ax2 = fig.add_subplot(222)
fig = sm.graphics.tsa.plot_pacf(log_df, lags=24, ax=ax2)

#%%
# Automatic ARIMA coeff determination 

# Fit auto_arima function to bike dataset
stepwise_fit = auto_arima(log_df['Total'], start_p=0, start_q=0, max_p = 2, max_q = 2) 

# To print the summary
stepwise_fit.summary()

#%%
(p,d,q) = (2,1,2)

#creation of the model with determined coeff
mod = SARIMAX(log_df, order = (p,d,q), seasonal_order = (p,d,q, 4))
res = mod.fit()

# Calculate MSE 
mean_square_error = res.mse
print(mean_square_error)

#We set date list
date_list = pd.date_range(start = max(log_df.index), end = '2021-04-02 00:00:00')
future = pd.DataFrame(index = pd.to_datetime(date_list), columns = ['Total'])
pred_df = pd.concat([pd.DataFrame(log_df), future])

# Get the exponential of the data
pred_log = res.predict(start = 0, end = len(pred_df))
pred = np.exp(pred_log)
print("Le nombre de vélos prévus pour le 02/04/2021 est de:", ceil(pred.iloc[-1]))

# Prediction
prediction = pred.iloc[-1] *0.20
print("Le nombre de vélos prévus pour le 02/04/2021, entre 00:00 et 09:00 est de:", ceil(prediction))
