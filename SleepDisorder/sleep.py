import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

dataset = pd.read_csv('sleep.csv')[['Gender', 'Age', 'Sleep Duration', 'Quality of Sleep', 'Physical Activity Level', 'Stress Level', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps', 'Sleep Disorder']]
dataset['Sleep Disorder'].fillna(0, inplace=True)
X, y = dataset.iloc[:,:-1], dataset.iloc[:,-1]
train_X, train_y, test_X, test_y = train_test_split(X, y, test_size=0.33, random_state=42)

clf = RandomForestClassifier(max_depth=5, random_state=0)
clf.fit(train_X, train_y)
