# Data source: https://www.kaggle.com/javierbravo/oil-price-and-share-price-of-a-few-companies
# License of data source: CC BY-SA 4.0
# Link to license: https://creativecommons.org/licenses/by-sa/4.0/
# Note: No changes were made to the data source.
# Uses keras, pands, sklearn, and numpy


from keras.layers import Dense, Flatten, Dropout
from keras.layers.convolutional import Conv1D, MaxPooling1D
from keras.models import Sequential
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import warnings
import matplotlib.pyplot as plt
import math

warnings.filterwarnings("ignore")

data = pd.read_csv("PMO.L.csv", encoding="utf-8")

ant_prices_list = []
guessed_prices_list = []

prices = []
shape = 4380;

i=0

while i < data.shape[0]:
    number = 0.0
    frame = data.iloc[i]
    value = frame["Close"]
    try:
        number = float(value)
        number = round(number, 2)
        if not math.isnan(number):
            prices.append(number)
    except:
         pass  
    i+=1
    
frame1 = None
frame2 = None
frame3 = None

i = 0
while i < shape - 3:

    if not frame1 is None:
        frame1 = frame2
        frame2 = frame3
        frame3 = prices[i+2]
          
    else:
        frame1 = prices[i]
        frame2 = prices[i+1]
        frame3 = prices[i+2]
  
    ant_prices = [frame1, frame2]
    guessed_price = frame3
    ant_prices_list.append(ant_prices)
    guessed_prices_list.append(guessed_price)
    i+=1       
       
x_train, x_test, y_train, y_test = train_test_split(ant_prices_list, guessed_prices_list, test_size = 0.2,
                                                    train_size = 0.8, shuffle =True)

x_train = np.reshape(x_train, (len(x_train), 2, 1))
x_test = np.reshape(x_test, (len(x_test), 2, 1))
                     
model = Sequential()

model.add(Conv1D(filters = 64, kernel_size=2, activation='relu', input_shape=(2,1)))
model.add(Conv1D(filters = 32, kernel_size=1, activation='relu'))
model.add(MaxPooling1D(pool_size=1))
model.add(Flatten())

model.add(Dense(32, activation='relu'))
model.add(Dense(1))


model.compile(optimizer='adam',loss='mse')

model.fit(x_train, y_train, batch_size=100, epochs = 10000, validation_split = 0.2, verbose=1)
result = model.evaluate(x_test, y_test)
print("\nEvaluation loss: ", result)
model.save("oil_prices.h5")
