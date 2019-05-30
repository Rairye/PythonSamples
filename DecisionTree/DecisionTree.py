# Data source: https://www.kaggle.com/yersever/500-person-gender-height-weight-bodymassindex/
# Source license: GPL 2
# Note: No changes have been made to the data set
# Requires sklearn and pandas

from sklearn import tree
import pandas as pd

weights_heights = pd.read_csv("500_Person_Gender_Height_Weight_Index.csv", encoding="utf-8")
features = weights_heights.loc[:, ["Height", "Weight", "Index"]]
labels =  weights_heights.loc[:, ["Gender"]]

running = True
prompt = True

decisionTree = tree.DecisionTreeClassifier()
decisionTree.fit(features, labels)


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
    
    print ("Result: {}".format(decisionTree.predict([[height, weight, index]])))


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
            
