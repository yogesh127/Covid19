import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import matplotlib.pyplot as plt 
import requests
import csv
import json

url = 'https://api.covid19india.org/data.json'

r = requests.get(url)

#print (r.json())

data = r.json()

tested = data['tested']

csvFile = open('tested.csv', 'w')

count = 0
csv_writer = csv.writer(csvFile)
for row in tested:
 if count == 0:
  headers = row.keys()
  csv_writer.writerow(headers)
  count=1
 csv_writer.writerow(row.values())
csvFile.close()

dataset = pd.read_csv('tested.csv')
dataset.shape
dataset.describe()

dataset.plot(x='totalindividualstested',y='totalsamplestested',style='o')

dataset.plot(x='totalindividualstested',y='totalpositivecases',style='o')

print(dataset.plot(x='totalsamplestested',y='totalpositivecases',style='o'))

X = dataset['totalsamplestested'].values.reshape(-1,1)
y = dataset['totalpositivecases'].values.reshape(-1,1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

X_train
y_train
cleanedList = [x for x in y_train if x != 'nan']
cleanedList
# y_train.type
y_train2 = y_train[~np.isnan(y_train)]
y_train2
dataset = dataset.dropna(axis=0, subset=['totalpositivecases'])
dataset
X = dataset['totalsamplestested'].values.reshape(-1,1)
y = dataset['totalpositivecases'].values.reshape(-1,1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
regressor = LinearRegression()  
regressor.fit(X_train, y_train) #training the algorithm
#To retrieve the intercept:
print(regressor.intercept_)
#For retrieving the slope:
print(regressor.coef_)

y_pred = regressor.predict(X_test)
y_pred
X_test
y_pred,X_test
y_pred = regressor.predict([[80000.]])
print(y_pred)