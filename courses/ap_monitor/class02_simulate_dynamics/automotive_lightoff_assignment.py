from pathlib import Path
from urllib.request import urlretrieve
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_name = "auto_warmup.txt"
url = 'http://apmonitor.com/pds/uploads/Main/' + file_name
file_path = Path(__file__).parent / file_name
if not file_path.is_file():
    urlretrieve(url, file_path)

data = pd.read_csv(file_path)

# set time index
data['time'] = pd.to_datetime(data['time'])
data = data.set_index('time')

print(data.info())

# Columns of interest
data1 = data[['Engine coolant temperature (℉)']].copy()
data1.dropna(inplace=True)
data2 = data[['Catalyst temperature Bank 1 Sensor 1 (℉)']].copy()
data2.dropna(inplace=True)
data3 = data[['Vehicle speed (mph)']].copy()

# Join data
data = data1.join(data2, how='outer', sort=True)
data = data.join(data3, how='outer', sort=True)
data.columns = ['coolant (degF)','catalyst (degF)','speed (mph)']
print(data.head())

# fill in NaNs - forward fill
data.ffill(inplace=True)
# fill in NaNs - backward fill
data.bfill(inplace=True)
dr = len(data)
data.describe()

# Plot data
data.plot(subplots=True, figsize=(10, 8))
plt.show()

# Remove outliers
data = data[data['coolant (degF)']>40]
data = data[data['speed (mph)']<20]

data['d1'] = data['coolant (degF)'].diff().abs()
data['d2'] = data['catalyst (degF)'].diff().abs()
data.plot(subplots=True,figsize=(10,6))
plt.show()


# Remove Other Outliers and Bad Speed Data
# 3 cycles because cat temperature stays high for a few samples
for i in range(3):
    data['d1'] = data['coolant (degF)'].diff().abs()
    data['d2'] = data['catalyst (degF)'].diff().abs()
    data = data[data['d1']<5]
    data = data[data['d2']<10]

# zero speed between 6:30 to 6:50
data.iloc[data.index.indexer_between_time('06:30','06:50'), 2] = 0

# delete d1 and d2
del data['d1']
del data['d2']

data.plot(subplots=True,figsize=(10,6))
print('Rows removed: ',dr-len(data), ' of ', dr)
plt.show()

# add engine state (on/off)
data['engine'] = 0
data.iloc[data.index.indexer_between_time('06:24:46','06:55:01'), 3] = 1

data.plot(subplots=True,figsize=(8,5))
plt.savefig('auto_warmup.png',dpi=300)
data.to_csv('auto_clean.csv')

# Determine Time to Catalyst Light-off
select = ['engine','catalyst (degF)']
s = data[select].between_time('06:24:40','06:26:00').copy()
s['light-off'] = (s['catalyst (degF)'] > 500).astype(int)
s.plot(subplots=True, figsize=(8, 5))
plt.show()

# find engine start time
for i in range(1,len(s)):
    if s['engine'].iloc[i]==1:
        engine_start = s.index[i]
        break

# find light-off time
for i in range(1,len(s)):
    if s['light-off'].iloc[i]==1:
        lightoff_start = s.index[i]
        break

# calculate seconds to catalyst light-off
dt = lightoff_start - engine_start
print(dt.total_seconds(), 'sec to catalyst light-off')

# Create ARX Model
# reduce data to about every 1-2 sec
data = data[::10].copy()

data['tmin'] = data.index
t0 = data['tmin'].iloc[0]
dt = (data['tmin'].copy()-t0)
dt2 = []
for i in range(len(data)):
    dt2.append(dt.iloc[i].total_seconds()/60.0)
data['tmin'] = dt2



from gekko import GEKKO

t = data['tmin'].values
u = data[['engine','speed (mph)']]
y = data[['catalyst (degF)','coolant (degF)']]

# generate time-series model
m = GEKKO(remote=False)

# system identification
na = 2 # output coefficients
nb = 40 # input coefficients
yp,p,K = m.sysid(t,u,y,na,nb,pred='meas')

plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(t,u)
plt.legend(['Engine','Speed (mph)'],loc=2)
plt.ylabel('Inputs')
plt.subplot(2,1,2)
plt.plot(t,y)
plt.plot(t,yp,'--')
plt.ylabel('Outputs')
plt.legend(['Catalyst (degF) Meas','Coolant (degF) Meas',\
            'Catalyst (degF) Pred','Coolant (degF) Pred'],loc=4)

plt.xlabel('Time (min)'); plt.savefig('sysid.png')
plt.show()
