import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fbprophet import Prophet
from sklearn.metrics import accuracy_score
import warnings
import json
from fbprophet.serialize import model_to_json, model_from_json
from sklearn.metrics import r2_score
from fbprophet.plot import plot_yearly
from dask.distributed import Client
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics

warnings.simplefilter('ignore')

df = pd.read_csv("../input/air-quality-data-in-india/station_hour.csv")
pm25 = df[['StationId', 'Datetime', 'PM2.5']]

max = 0
min = 99999
for i in pm25.loc[:, 'StationId'].unique():
    alpha = pm25.loc[pm25.loc[:, 'StationId'] == i]
    alpha.dropna(inplace=True)
    try:
        a = len(alpha)
        b = len(pd.date_range(start=str(alpha.iloc[0, 1]), end=str(alpha.iloc[-1, 1]), freq='D').difference(
            alpha.iloc[:, 1]))
        print(i + '\t' + a + '\t' + b + '\t' + (a - b))
        if (a - b) > max:
            max = a - b
            beta = i
        if b < min:
            min = b
            gamma = i
    except:
        print(i)
print("MAX Difference:\t", beta)
print("MIN Missing:\t", gamma)

client = Client()

pm25_UP012 = pm25.loc[pm25.loc[:, 'StationId'] == 'UP012']
pm25_UP012.pop('StationId')
pm25_UP012.columns = ['ds', 'y']
pm25_UP012.dropna(inplace=True)
pm25_UP012_train = pm25_UP012.iloc[:-int(len(pm25_UP012) * 0.1), :]
pm25_UP012_test = pm25_UP012.iloc[-int(len(pm25_UP012) * 0.1):, :]

m = Prophet(weekly_seasonality=False, yearly_seasonality=20)
m.add_country_holidays(country_name='IN')
m.add_seasonality(name='monthly', period=30.5, fourier_order=5)

m.fit(pm25_UP012_train)

future = m.make_future_dataframe(periods=30, freq='D', include_history=True)
forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
plt.figure(figsize=(15, 10))
fig1 = m.plot(forecast)
plt.show(fig1)

a = plot_yearly(m)

pm25_UP012_test['ds'] = [str(x) for x in pm25_UP012_test['ds']]
forecast['ds'] = [str(x) for x in forecast['ds']]

pm25_UP012['ds'] = [str(x) for x in pm25_UP012['ds']]

y = []
yhat = []

for i in [x for x in pm25_UP012['ds']]:
    #     print(i)
    if i in [x for x in forecast['ds']]:
        print(i)
        y.append(pm25_UP012.iloc[[x for x in pm25_UP012['ds']].index(i), -1])
        yhat.append(forecast.iloc[[x for x in forecast['ds']].index(i), -1])

r2_score(y, yhat)

with open('serialized_model.json', 'w') as fout:
    json.dump(model_to_json(m), fout)  # Save model

with open('serialized_model.json', 'r') as fin:
    m = model_from_json(json.load(fin))  # Load model
