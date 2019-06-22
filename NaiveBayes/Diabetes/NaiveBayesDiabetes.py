# Data source: https://www.kaggle.com/uciml/pima-indians-diabetes-database
# License of data source: CC0: Public Domain
#Requires pandas, sklearn, and numpy

import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.naive_bayes import GaussianNB

patient_data = pd.read_csv("diabetes.csv", encoding="utf-8").astype('float64')

features = patient_data.loc[:, ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]]
labels = patient_data.loc[:, ["Outcome"]]


x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size = 0.3,
                                                    train_size = 0.7, shuffle =True)


y_train = np.ravel(y_train)
y_test = np.ravel(y_test)


model = GaussianNB()
model.fit(x_train, y_train)

score = model.score(x_test, y_test)
print("\nScore: ", str(round(score * 100, 2) ) + "%")
