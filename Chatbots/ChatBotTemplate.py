# Requires pandas and sklearn

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

#Define name of the CSV file containing the corpus.
file_name = ""
#Define name of the CSV column in which the question text is located.
question_column = ""
#Define name of the CSV column in which the answer text is located.
answer_column = ""
lines = pd.read_csv(file_name, encoding="utf-8")

tfidf_vectorizer = TfidfVectorizer()
inputs_outputs = {}
inverted_index = {}
inputs = []

def normalize_text(line):
    line = line.lower()
    line = line.translate(str.maketrans('', '', "\"$.?1%&/'()*+,;<=>[\]^_`{|}~\n“”’\ufeff"))
    return line

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
    indices = set([])
    cosine_sim = 0
    responses = []
    
    for word in words:
        if word not in inverted_index:
            continue
        
        numbers = inverted_index[word]
        for number in numbers:
            indices.add(number)
    
    for index in indices:
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
       
             
    if len(responses) == 0:
        return "I don't know what you are talking about."
    else:
        return random.choice(responses)

shape = lines.shape[0]
i = 0

while i < shape-1:
    this_line = lines.iloc[i]  
    question = this_line[question_column]
    answer = this_line[answer_column]
    norm_frame1 = normalize_text(question)
    inputs_outputs[norm_frame1] = answer
    inputs.append(norm_frame1)
    update_inverted_index(norm_frame1)
    i+=1

running = True
print("\n\nType \"See ya\" to exit.\n")

while running:
    user_input = input(": ")
    norm_input = normalize_text(user_input) if user_input != "" else None
    print("...")
    if norm_input == "see ya":
        print("\nSee ya\n")
        running = False
        break
    if norm_input != None:
        print("> " + get_response(norm_input))
