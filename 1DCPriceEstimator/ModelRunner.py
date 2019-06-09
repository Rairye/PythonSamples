#Uses keras and numpy

from keras.models import load_model
import numpy as np

model = load_model("oil_prices.h5")

def get_prediction(day_one = 0.0, day_two = 0.0):
    input_predict = np.array([day_one, day_two])
    input_predict = np.reshape(input_predict, (1, 2, 1))
    result = model.predict(input_predict)
    result_number = result[0][0]
    return round(result_number, 6)

value_one = 0.0
value_two = 0.0

value_one_input = False
value_two_input = False

while value_one_input == False:
    input_one = input("\n\nDay one closing price: ")
    
    try:
        value_one = float(input_one)
        value_one = round(value_one, 6)
        value_one_input = True
    except:
        print("Invalid number. Please try again.")
    
while value_two_input == False:
    input_two = input("Day two closing price: ")
    
    try:
        value_two = float(input_two)
        value_two = round(value_two, 6)
        value_two_input = True
    except:
        print("Invalid number. Please try again.")

print("Day three estimated closing price: ", get_prediction(value_one, value_two))
