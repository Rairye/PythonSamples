# Generator of random sentences from corpus, using bi-grams.
# Data source: https://www.kaggle.com/pierremegret/dialogue-lines-of-the-simpsons
# License: CC BY-SA 3.0
# Link to license: https://creativecommons.org/licenses/by-sa/3.0/
# Note: The data source has not been altered.
# Requires pandas and nltk

import pandas as pd
import random
from nltk.tokenize import PunktSentenceTokenizer
from collections import OrderedDict
from nltk.corpus import stopwords

def strip_punct(line):
    line = line.strip()
    line = line.replace("  ", " ", 30)
    return line

def normalize_word(word):
    word = word.translate(str.maketrans('', '','/:()"'))
    if '--' in word:
        word = word.replace('--', '', 30)
    word = word.strip()
    return word

lines = pd.read_csv("simpsons_dataset.csv", encoding="utf-8")
shape = lines.shape[0] 
i = 0

word_pairs = {}
tokenizer = PunktSentenceTokenizer()
stop_words = set(stopwords.words('english'))

while i < shape:
    
    line = lines.iloc[i]
    frame1 = line["spoken_words"]
    
    if type(frame1) is str:
        sent_tokens = tokenizer.tokenize(frame1)
        
        for sent in sent_tokens:
            sent = strip_punct(sent)
            word_tokens = sent.split(" ")
            scope = len(word_tokens) -1
            j = 0
            if len(word_tokens) > 2:
                while j <= scope:
                    first_word = normalize_word(word_tokens[j]) if j > 1 else normalize_word(word_tokens[0]) if j == 1 else "###BOUNDARY" 
                    second_word = "###BOUNDARY" if j == scope else normalize_word(word_tokens[j]) if j == 0 else normalize_word(word_tokens[j+1])
                    
                    if first_word not in word_pairs or (first_word in word_pairs and word_pairs[first_word] == {}): 
                        word_pairs[first_word] = {second_word : 1}
                    else:
                        temp_dict = word_pairs[first_word]
                       
                        if second_word in temp_dict:
                            count = temp_dict[second_word]
                            temp_dict[second_word] = count+1
                        else:
                            temp_dict[second_word] = 1

                        word_pairs[first_word] = temp_dict

                    if second_word not in word_pairs:
                        word_pairs[second_word] = {}

                    j+=1
            
    i+=1

def get_sent():
    result = ''
    second_word = ''
    start_word_dict = word_pairs["###BOUNDARY"]
    start_word = random.choice(list(start_word_dict.keys()))
    result = result + start_word
    
    running = True

    second_word = start_word
    
    while running:
       
        word_dict = word_pairs[second_word]
        temp = OrderedDict(sorted(word_dict.items(), key=lambda t: t[1], reverse = True))
        keys = list(temp.keys())
        values = list(temp.values())
        words = [keys[0]]
        max_len = values[0]         
        maxed = False
        scope = 0
      
        if keys[0] == "###BOUNDARY":
            running = False
            return result
            
        if len(values) > 1:
            while maxed == False and scope < len(values) - 1:
                if values[scope+1] == max_len:
                    words.append(keys[scope])
                    scope+=1
                else:
                    maxed = True
                    
            #Prevents infinite loops
            if len(words) == 1 and words[0].lower() in stop_words:
                second_word = random.choice(keys)
            else:
                second_word = random.choice(words)

        else:
            second_word = keys[0]
        
        if second_word == "###BOUNDARY":
            running = False
        else:
            #Prevents infinite loops
            if (result).endswith(second_word):
                if len(values) > 1:
                    second_word = random.choice(keys)
                if second_word == "###BOUNDARY":
                    running = False
                else:
                    running = False
            
            result = result + " " + second_word   
        
    return result
    
print("\n")    
print(get_sent() + "\n")
print(get_sent() + "\n")   
print(get_sent() + "\n")
print(get_sent() + "\n") 
