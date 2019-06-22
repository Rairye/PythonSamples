# Data source: https://www.kaggle.com/team-ai/spam-text-message-classification/downloads/spam-text-message-classification.zip/1
# License type: Creative commons
# Requires pandas, sklearn, numpy, and tensorflow

import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing.text import Tokenizer
import re
import numpy as np
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from sklearn.naive_bayes import BernoulliNB

messages = pd.read_csv("SPAM text message 20170820 - Data.csv", encoding="utf-8")


text = []
spam = []
max_tokens = 0
shape = messages.shape[0]
i = 0

while i < shape:
    try:
        frame = messages.iloc[i]
        message = frame["Message"]
        message_type = frame["Category"]
        split = message.split()
        result = ""
        j = 0
        k = 0
        while j < len(split):
            word = split[j]
            word = word.strip()
            word = word.translate(str.maketrans('', '', "\"$.?1%&'()*+,:;<=>[\]^_`{|}~“”’"))                 
            if (re.match('^[a-zA-Z0-9.?!-#]+$', word)):
                result = result + word
                if j < (len(split) - 1):
                    result = result + " "
                k += 1
            j +=1
        if j > max_tokens:
            max_tokens = k  
        text.append(result)
        
        
        if message_type == "ham":
            spam.append(0)
        if message_type == "spam":
            spam.append(1)
          
        
        i +=1
    except Exception as e:
        print(e)
        i +=1

tk = Tokenizer(None, filters='')
tk.fit_on_texts(text)
word_to_int = tk.word_index

x_train, x_test, y_train, y_test = train_test_split(text, spam, test_size = 0.3,
                                                    train_size = 0.7, shuffle =True)

x_train_tokens = tk.texts_to_sequences(x_train)
x_test_tokens = tk.texts_to_sequences(x_test)



padded_x_train = pad_sequences(x_train_tokens, maxlen=max_tokens, padding='pre', truncating='pre')
padded_x_test = pad_sequences(x_test_tokens, maxlen=max_tokens, padding='pre', truncating='pre')


model = BernoulliNB()
model.fit(padded_x_train, y_train)
score = model.score(padded_x_test, y_test)
print("\nNumber of samples in dataset: ", shape)
print("Score: ", str(round(score * 100, 2) ) + "%")


