# Data source: https://www.kaggle.com/crowdflower/twitter-airline-sentiment/
# Data source license: CC BY-NC-SA 4.0  Link: https://creativecommons.org/licenses/by-nc-sa/4.0/
# Note: No changes were made to the data source
# Requires pandas, sklearn, numpy, tensorflow, and keras

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing.text import Tokenizer
import re
import numpy as np
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, GRU, Embedding, Dropout
import warnings

warnings.filterwarnings("ignore")

tweets = pd.read_csv("Tweets.csv", encoding="utf-8")
text = []
sentiments = []
max_tokens = 0
shape = tweets.shape[0]
i = 0

while i < shape:
    try:
        frame = tweets.iloc[i]
        tweet = frame["text"]
        sentiment = frame["airline_sentiment"]
        split = tweet.split()
        result = ""
        j = 0
        k = 0
        while j < len(split):
            word = split[j]
            word = word.strip()
            word = word.translate(str.maketrans('', '', "\"$.?!%&/'()*+,:;<=>[\]^_`{|}~“”’"))
            if not word.startswith("@"):                    
                if (re.match('^[a-zA-Z0-9.?!-#]+$', word)):
                    result = result + word
                    if j < (len(split) - 1):
                        result = result + " "
                    k += 1
            j +=1
        if j > max_tokens:
            max_tokens = k  
        text.append(result)
        
        
        if sentiment == "negative":
            sentiments.append(0)
        if sentiment == "neutral" or sentiment == "positive":
            sentiments.append(1)
          
        
        i +=1
    except Exception as e:
        print(e)
        i +=1

tk = Tokenizer(None, filters='')
tk.fit_on_texts(text)


x_train, x_test, y_train, y_test = train_test_split(text, sentiments, test_size = 0.3,
                                                    train_size = 0.7, shuffle =True)

x_train_tokens = tk.texts_to_sequences(x_train)
x_test_tokens = tk.texts_to_sequences(x_test)


padded_x_train = pad_sequences(x_train_tokens, maxlen=max_tokens, padding='pre', truncating='pre')
padded_x_test = pad_sequences(x_test_tokens, maxlen=max_tokens, padding='pre', truncating='pre')


model = Sequential()
model.add(Embedding(input_dim=len(tk.word_index)+1,
                    output_dim=10,
                    input_length = max_tokens))

model.add(GRU(units=8, return_sequences=True))

model.add(GRU(units=4, return_sequences=True))
model.add(GRU(units=2, return_sequences=False))
model.add(Dropout(0.5))
model.add(Dense(1, activation="sigmoid"))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


try:
    model.fit(np.array(padded_x_train), np.array(y_train), validation_split = 0.1, epochs=100, batch_size=400, verbose = 1)
    result = model.evaluate(np.array(padded_x_test), np.array(y_test))
    print("\nResult: ", result)
except Exception as e:
    print("Excpetion: ", e)

