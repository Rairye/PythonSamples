# Data source: https://www.kaggle.com/dryad/baboon-mating
# License of data source: CC0: Public Domain
#Requires pandas, sklearn, numpy, and matplotlib

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import roc_auc_score
import numpy as np
import matplotlib.pyplot as plt

breeding_data = pd.read_csv("baboon_mating.csv", encoding="utf-8")

female_alpha_to_int = {}
female_int_to_alpha = {}
male_alpha_to_int = {}
male_int_to_alpha = {}

shape = breeding_data.shape[0]
i = 0

while i < shape:
    frame = breeding_data.iloc[i]
    female_id = frame["female_id"]
    male_id = frame["male_id"]
    if female_id not in female_alpha_to_int:
        female_alpha_to_int[female_id] = len(female_alpha_to_int)
        female_int_to_alpha[len(female_int_to_alpha)] = female_id
    
    breeding_data.iat[i, 0] = female_alpha_to_int[female_id]
   
    if male_id not in male_alpha_to_int:
        male_alpha_to_int[male_id] = len(male_alpha_to_int)
        male_int_to_alpha[len(male_int_to_alpha)] = male_id
    
    breeding_data.iat[i, 1] = male_alpha_to_int[male_id]
 
    i+=1

breeding_data[["female_id"]] = breeding_data[["female_id"]].astype(np.int64)
breeding_data[["female_id"]] = breeding_data[["male_id"]].astype(np.int64)
breeding_data[["male_gendiv"]] = breeding_data[["male_gendiv"]].astype(np.float64)

breeding_data = breeding_data.round({"female_hybridscore": 4, "male_hybridscore" : 4, "femalee_age" : 4, "male_rank_transform" : 4, "gen_distal" : 4})

features = breeding_data.loc[:, ["female_id", "male_id", "cycle_id", "consort", "female_hybridscore", "male_hybridscore", "female_gendiv", "male_gendiv", "gen_distance", "female_age", "male_rank", "female_rank", "males_present", "females_present", "male_rank_transform", "gen_distance_transform", "rank_interact" ]]
conceptive = breeding_data.loc[:,["conceptive"]]
conceptive = np.ravel(conceptive)

model = RandomForestRegressor(n_estimators = 200, oob_score = True, random_state = 20)
model.fit(features, conceptive)

print("Oob score: ", model.oob_score_)
print("ROC AUC score: ", roc_auc_score(conceptive, model.oob_prediction_))

important_features = pd.Series(model.feature_importances_, index= features.columns)
important_features.sort_values()
important_features.plot(kind="barh", figsize = (15,15))
plt.show()
