#Data set source: Mohan S Acharya, Asfia Armaan, Aneeta S Antony : A Comparison of Regression Models for Prediction of Graduate Admissions, IEEE International Conference on Computational Intelligence in Data Science 2019
# Data link: https://www.kaggle.com/mohansacharya/graduate-admissions#Admission_Predict_Ver1.1.csv
# Dataset license: CC0: Public Domain
#Requires pandas, numpy, and sklearn

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


data = pd.read_csv('Admission_Predict_Ver1.1.csv', encoding='utf-8')

train_features = []
test_features = []
train_target = []
test_target = []
   
rows = (data.shape[0])

test_range = int(data.shape[0] * .3)

i = 0

while i < test_range:
    frame = data.iloc[i]
    test_features.append([frame["GRE Score"], frame["TOEFL Score"], frame["University Rating"], frame["SOP"], frame["LOR "], frame["CGPA"], frame["Research"]])
    test_target.append(frame["Chance of Admit "])
    i += 1
    
while i < data.shape[0]:
    
    frame = data.iloc[i]
    train_features.append([frame["GRE Score"], frame["TOEFL Score"], frame["University Rating"], frame["SOP"], frame["LOR "], frame["CGPA"], frame["Research"]])
    train_target.append(frame["Chance of Admit "])
    i += 1

regression = LinearRegression(normalize=True)
regression.fit(train_features, train_target)


def predict(gre_score, toefl_score, university_rating, sop, lor, cgpa, research):
    result = str(regression.predict([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]]))
    resultNumber = round(float(result[1:-1]), 4)
    print("Prediction result: {}%".format(resultNumber * 100))
    print("Prediction score: {}%".format(round(regression.score(test_features, test_target), 4) * 100))


running = input_gre_score = input_toefl_score = input_university_rating = input_sop = input_lor = input_cgpa = input_research = True


while running == True:

    gre_score = toefl_score = university_rating = research = 0
    sop = lor= cgpa = 0.0
    run_again = True
    running = False
    

predict(337, 118, 4, 4.5, 4.5, 9.65, 1)

