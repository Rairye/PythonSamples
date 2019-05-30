# Data source: https://www.kaggle.com/dryad/baboon-mating
# License of data source: CC0: Public Domain
#Requires pandas, sklearn, and numpy


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np


breeding_data = pd.read_csv("baboon_mating.csv", encoding="utf-8")

features = breeding_data.loc[:, ["conceptive", "consort", "female_hybridscore", "male_hybridscore", "female_gendiv", "male_gendiv", "gen_distance", "female_age"]]

print("Clustering...")
clusters = MeanShift(estimate_bandwidth(features, quantile=0.2, n_samples=500)).fit(features)

print("Number of clusters found: {}".format(len(np.unique(clusters.labels_))))


running = input_consort = input_conceptive = input_female_hybrid_score = input_male_hybrid_score = input_female_gendiv = input_male_gendiv = input_gen_distance = input_female_age = True


def prediction(consort, conceptive, female_hybridscore, male_hybridscore, female_gendiv, male_gendiv, gen_distance, female_age):
    arguments = [[consort, female_hybridscore, male_hybridscore, female_gendiv, male_gendiv, gen_distance, female_age]]
    result = clusters.predict([[consort, conceptive, female_hybridscore, male_hybridscore, female_gendiv, male_gendiv, gen_distance, female_age]])
    print("Cluster: ", result[1])
    
while running == True:

      consort = conceptive = 0
      female_hybrid_score = male_hybrid_score = female_gendiv = male_gendiv = gen_distance = female_age = 0.0
      run_again = True
      
      while input_consort == True:
          temp = input("Consort (0 or 1): ")
          try:
              consort = int(temp)
              if consort == 0 or consort == 1:
                  input_consort = False
          except:
              pass
            
      while input_conceptive == True:
          temp = input("Conceptive (0 or 1): ")
          try:
              conceptive = int(temp)
              if conceptive == 0 or conceptive == 1:
                  input_conceptive = False
          except:
              pass
            
      while input_female_hybrid_score == True:
          temp = input("Female hydrid score (float between 0.0 and 1.0): ")
          try:
              female_hybrid_score = float(temp)
              if female_hybrid_score >= 0.0 and female_hybrid_score <= 1.0:
                  input_female_hybrid_score = False
          except:
              pass
        
      while input_male_hybrid_score == True:
          temp = input("Male hybrid score (float between 0.0 and 1.0): ")
          try:
              male_hybrid_score = float(temp)
              if male_hybrid_score >= 0.0 and male_hybrid_score <= 1.0:
                  input_male_hybrid_score = False
          except:
              pass

      while input_female_gendiv == True:
          temp = input("Female gendiv (float between 0.0 and 1.0): ")
          try:
              female_gendiv = float(temp)
              if female_gendiv >= 0.0 and female_gendiv <= 1.0:
                  input_female_gendiv = False
          except:
              pass

      while input_male_gendiv  == True:
          temp = input("Male gendiv (float between 0.0 and 1.0): ")
          try:
              male_gendiv = float(temp)
              if male_gendiv >= 0.0 and male_gendiv <= 1.0:
                  input_male_gendiv = False
          except:
              pass
            
      while input_gen_distance  == True:
          temp = input("Gen distance (float between -1.0 and 1.0): ")
          try:
              gen_distance = float(temp)
              if gen_distance >= -1.0 and gen_distance <= 1.0:
                  input_gen_distance = False
          except:
              pass
      while input_female_age  == True:
          temp = input("Female age (positive float): ")
          try:
              female_age = float(temp)
              if female_age >= 0.0:
                  input_female_age = False
          except:
              pass
      prediction(consort, conceptive, female_hybrid_score, male_hybrid_score, female_gendiv, male_gendiv, gen_distance, female_age)

      while run_again == True:
          result = input("\nRun again? (Y/N): ")
          
          if result == "N" or result == "n":
              run_again = False
              running = False
              
          if result == "Y" or result == "y":
              run_again = False
              input_consort = True
              input_female_hybrid_score = True
              input_male_hybrid_score = True
              input_female_gendiv = True
              input_male_gendiv = True
              input_gen_distance = True
              input_female_age = True

      prompt = True
