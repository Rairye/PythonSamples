# Data source: https://www.kaggle.com/yersever/500-person-gender-height-weight-bodymassindex/
# Source license: GPL 2
# Note: No changes have been made to the data set
# Requires sklearn and pandas


from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import warnings
warnings.filterwarnings("ignore")

weights_heights = pd.read_csv("500_Person_Gender_Height_Weight_Index.csv", encoding="utf-8")

features = []
genders = []

no_of_rows = weights_heights.shape[0]
i = 0

while i < no_of_rows:
    frame = weights_heights.iloc[i]
    features.append([frame["Height"], frame["Weight"], frame["Index"]])
    gender = 0 if frame["Gender"] == "Male" else 1
    genders.append(gender)
    i+=1

x_train, x_test, y_train, y_test = train_test_split(features, genders, test_size = 0.5, train_size = 0.5)

running = True
prompt = True

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, np.ravel(y_train))

def getResult(height, weight, index):

    try:
        height = int(height)
        weight = int(weight)
        body_type = int(index)
    except:
        if type(height) != int:
            print ("Invalid argument: Height must be a number.")
        if type(weight) != int:
            print ("Invalid argument: Weight must be a number.")
        if type(index) != int:
            print("Body type must be a number")
        return
    
    if height < 0 or weight < 0 or (body_type < 0 or body_type > 5):
         if height < 0:
            print("Height must be a positive number.")
         if weight < 0:
            print("Weight must be a positive number.")
         if body_type <  0 or body_type > 5:
            print("Body type must be between 0 and 4")
         return
    
    print ("Result: {}".format("Male" if knn.predict([[height, weight, index]]) == [0] else "Female"))


while running == True:

      height = input("Height (centimers): ")
      weight = input("Weight (kilograms): ")
      body_type = input("Input extra information (0: Extremely underweight, 1: Underweight, 2: Normal, 3: Overweight, 4: Obese, 5: Extremely obese): ")  
      getResult(height, weight, body_type)

      while prompt == True:
          result = input("Run again? (Y/N): ")
          
          if result == "N" or result == "n":
              prompt = False
              running = False
              
          if result == "Y" or result == "y":
              prompt = False

      prompt = True
            
