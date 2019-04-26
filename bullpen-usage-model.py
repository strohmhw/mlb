# Import Libraries
import datetime, time
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

# Import Datasets
three_day_usage = pd.read_csv('three_day_usage.csv')
seven_day_usage = pd.read_csv('seven_day_usage.csv')
thirty_day_usage = pd.read_csv('thirty_day_usage.csv')
current_day_result = pd.read_csv('current_day_result.csv')

# Create Unique Tm_Date Identifiers
three_day_usage['Tm_Date'] = three_day_usage['Tm'] + three_day_usage['Date']
seven_day_usage['Tm_Date'] = seven_day_usage['Tm'] + seven_day_usage['Date']
thirty_day_usage['Tm_Date'] = thirty_day_usage['Tm'] + thirty_day_usage['Date']
current_day_result['Tm_Date'] = current_day_result['Tm'] + current_day_result['Date']

# Create Train/Test Set
dataset = pd.DataFrame()
dataset = three_day_usage[['Tm_Date', 'Date', 'Tm', 'TBF']]
dataset = pd.merge(dataset, seven_day_usage[['Tm_Date', 'TBF']], on="Tm_Date", how="left")
dataset = pd.merge(dataset, thirty_day_usage[['Tm_Date', 'xFIP']], on="Tm_Date", how="left")
dataset = pd.merge(dataset, current_day_result[['Tm_Date', 'FIP']], on="Tm_Date", how="left")
dataset.columns = ['Tm_Date', 'Date', 'Tm', '3day_TBF', '7day_TBF', 'past_xFIP', 'result_FIP']
dataset = dataset[np.isfinite(dataset['result_FIP'])]

# Machine learning Algorithm
linear = linear_model.LinearRegression()

df = dataset[['7day_TBF']]
y = dataset['result_FIP']

X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2)

model = linear.fit(X_train, y_train)
score = linear.score(X_test, y_test)
predictions = linear.predict(X_test)

plt.scatter(y_test, predictions)
plt.xlabel(“True Values”)
plt.ylabel(“Predictions”)

print(score)
