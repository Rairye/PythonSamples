# Chat bot based on lines from The Simpsons. Responses are printed to the console and also provided using TTS.
# Data source: https://www.kaggle.com/pierremegret/dialogue-lines-of-the-simpsons
# License: CC BY-SA 3.0
# Link to license: https://creativecommons.org/licenses/by-sa/3.0/
# Note: The data source has not been altered.
# Requires pandas, sklearn, and pyttsx3

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
from collections import OrderedDict
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    if voice.name.endswith("English (United States)"):
        engine.setProperty('voice', voice.id)
        break

volume = engine.getProperty("volume")
engine.setProperty("volume", volume + 0.5)

rate = engine.getProperty("rate")
engine.setProperty("rate", rate-0.1)

lines = pd.read_csv("simpsons_dataset.csv", encoding="utf-8")

tfidf_vectorizer = TfidfVectorizer()
inputs_outputs = {}
inverted_index = {}
inputs =[]
frame1 = None
frame2 = None

def normalize_text(line):
    line = line.lower()
    line = line.translate(str.maketrans('', '', "\"$.?1%&/'()*+,;<=>[\]^_`{|}~\n“”’\ufeff"))
    return line

def speak(line):
    if line == "D'oh!":
        line = "Dough!"

    engine.say(line)
    engine.runAndWait()
    engine.stop()

def update_inverted_index(sentence):
    split = set(sentence.split(" "))

    for word in split:
        if word not in inverted_index:
            inverted_index[word] = [len(inputs)-1]
        else:
            temp = inverted_index[word]
            temp.append(len(inputs)-1)
            inverted_index[word] = temp

def get_response(user_input):
    words = set((user_input).split(" "))
    indices = {}
    cosine_sim = 0
    responses = []
    
    for word in words:
        if word not in inverted_index:
            continue
        
        numbers = inverted_index[word]
        for number in numbers:
            if number not in indices:
                indices[number] = 1
            else:
                value = indices[number]
                indices[number] = value + 1
    
    sorted_indices = OrderedDict(sorted(indices.items(), key=lambda t: t[1], reverse = True)) if len(indices) > 0 else None
    max_value = list(sorted_indices.values())[0] if sorted_indices != None else None

    if sorted_indices == None:
        return "D'oh!"
    
    for index in sorted_indices:
        if sorted_indices[index] < max_value:
            break
        
        input_phrase = inputs[index]      
        comparison = [input_phrase, user_input]
        matrix = tfidf_vectorizer.fit_transform(comparison)
        sim = cosine_similarity(matrix[0], matrix[1])
        sim_num = round(sim[0][0], 2)

        if sim_num == cosine_sim:
            responses.append(inputs_outputs[input_phrase])
            
        if sim_num > cosine_sim:
            cosine_sim = sim_num
            responses = [inputs_outputs[input_phrase]]
       
    return random.choice(responses)

shape = lines.shape[0]
i = 0

while i < shape-1:

    if frame1 == None and frame2 == None:
        this_line = lines.iloc[i]
        next_line = lines.iloc[i+1]
        frame1 = this_line["spoken_words"]
        frame2 = next_line["spoken_words"]
        if type(frame1) is str and type(frame2) is str:
            norm_frame1 = normalize_text(frame1)
            inputs_outputs[norm_frame1] = frame2
            inputs.append(norm_frame1)
            update_inverted_index(norm_frame1)
            i+=1
            
        else:
            i = i + 1 if not type (frame1) is str else i + 2
            frame1 = None
            frame2 = None
    else:
        frame1 = frame2
        next_line = lines.iloc[i+1]
        frame2 = next_line["spoken_words"]
        if not type(frame2) is str:
            i+=2
            frame1 = None
            frame2 = None
        else:
            norm_frame1 = normalize_text(frame1)
            inputs_outputs[norm_frame1] = frame2
            inputs.append(norm_frame1)
            update_inverted_index(norm_frame1)
            i+=1 

running = True
print("\n\nType \"Smell ya later\" to exit.\n")

while running:
    user_input = input(": ")
    norm_input = normalize_text(user_input) if user_input != "" else None
    print("...")
    if norm_input == "smell ya later":
        print("\nSmell ya later\n")
        speak("Smell ya later")
        running = False
        break
    if norm_input != None:
        response = get_response(norm_input)
        print("> " + response)
        speak(response)
