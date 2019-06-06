# Data source: https://www.kaggle.com/CooperUnion/anime-recommendations-database/downloads/anime-recommendations-database.zip/1
# Data source license: CC0: Public Domain
# Uses pandas, sklearn, numpy, tensorflow, and keras

import pandas as pd
import warnings
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Model
from keras.layers import Input, Embedding, Flatten, Concatenate, Dense, Dropout
import random

warnings.filterwarnings("ignore")

anime_names = pd.read_csv("anime.csv", encoding="utf-8")
user_data = pd.read_csv("rating.csv", encoding="utf-8")

name_id_dict = {}
id_name_dict = {}

shape = anime_names.shape[0]
i = 0

while i < shape:
    try:
        frame = anime_names.iloc[i]
        anime_name = frame["name"]
        anime_id = frame["anime_id"]
        name_id_dict[anime_name] = anime_id
        id_name_dict[anime_id] = anime_name
        i += 1
    except Exception as e:
        print("Exception: ", e)

user_id_test = []
user_id_train = []

anime_id_test = []
anime_id_train = []

ratings_test = []
ratings_train = []

user_id_set = set()
anime_id_set = set()
user_id_set_max = 0
anime_id_set_max = 0


shape = user_data.shape[0]
i = 0
test_size = int(shape * .3)


while i < shape:
    try:
        frame = user_data.iloc[i]
        user_id = frame["user_id"]
        anime_id = frame["anime_id"]
        rating = frame["rating"]
        shuffle_number = random.randint(0,2)
        
        if shuffle_number == 0 and len(ratings_test) <= test_size:  
            user_id_test.append(user_id)
            anime_id_test.append(anime_id)
            ratings_test.append(rating)
            
        else:
            user_id_train.append(user_id)
            anime_id_train.append(anime_id)
            ratings_train.append(rating)
        
        user_id_set.add(user_id)
        anime_id_set.add(anime_id)
        
        if user_id > user_id_set_max:
            user_id_set_max = user_id
        
        if anime_id > anime_id_set_max:
            anime_id_set_max = anime_id
            
        i += 1
    
    except Exception as e:
        print("Exception: ", e)

user_id_test = np.array(user_id_test)
user_id_train = np.array(user_id_train)

anime_id_test = np.array(anime_id_test)
anime_id_train = np.array(anime_id_train)

ratings_test = np.array(ratings_test)
ratings_train = np.array(ratings_train)


user_id_input = Input(shape=[1])
anime_id_input = Input(shape=[1])

user_id_embedding = Embedding(input_dim=user_id_set_max + 1, output_dim=10)(user_id_input)
flattened_user_id = Flatten()(user_id_embedding)

anime_id_embedding = Embedding(input_dim=anime_id_set_max + 1, output_dim=10)(anime_id_input)

flattened_anime_id = Flatten()(anime_id_embedding)
joined = Concatenate()([flattened_user_id, flattened_anime_id])

dense1 = Dense(128, activation='relu')(joined)
dropout = Dropout(0.01)(dense1)
dense2 = Dense(32, activation='relu')(dropout)

dense3 = Dense(1)(dense2)

model = Model([user_id_input, anime_id_input], dense3)
model.compile('Adam', 'mean_squared_error', metrics=['accuracy'])
print(model.summary())

try:
    model.fit([user_id_train , anime_id_train], ratings_train, epochs=1000, batch_size = 1000, validation_split=0.2, verbose = 1)
    result = model.evaluate([user_id_test, anime_id_test], ratings_test, batch_size = 1000)
    print("Result: ", result)
    model.save('recommendation_model1.h5')
except Exception as e:
    print("Exception: ", e)

print("Finished")
