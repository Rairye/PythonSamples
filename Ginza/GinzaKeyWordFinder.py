#キーワードを探すためのスクリプト
#Uses Ginza and spaCy
import spacy
from collections import OrderedDict

nlp = spacy.load("ja_ginza")
lines = open(fileName, encoding='utf-8')
word_counts = {}
noun_types = set(["NOUN", "PRON", "PROPN"])
other_types = set(["VERB", "ADJ", "ADV"])

def update_counts(word):
    if word in word_counts:
        temp_count = word_counts[word]
        word_counts[word] = temp_count + 1
    else:
        word_counts[word] = 1

for line in lines:
    noun_components = []
    nlp_line = nlp(line)
    for sent in nlp_line.sents:
        for token in sent:
            if token.pos_ in noun_types:
                noun_components.append(token.orth_)
            else:
                if len(noun_components) >= 1:
                    update_counts(''.join(noun_components)) 
                noun_components = []
                
            if token.pos_ in other_types:
                word = token.orth_
                update_counts(word)
                
        if len(noun_components) >= 1:
            update_counts(''.join(noun_components))

temp = OrderedDict(sorted(word_counts.items(), key=lambda t: t[1], reverse = True))
results = temp
for key in results.keys():
    print(key, ": ", results[key])
