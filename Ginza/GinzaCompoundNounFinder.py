#新規な複合名詞を探すためのスクリプト
#Uses Ginza and spaCy
import spacy
nlp = spacy.load("ja_ginza")

compound_nouns = []

fileName = ""
lines = open(fileName, encoding='utf-8')

for line in lines:
    noun_components = []
    nlp_line = nlp(line)
    for sent in nlp_line.sents:
        for token in sent:
            print(token)
            if token.pos_ == "NOUN":
                noun_components.append(token.orth_)
            else:
                if len(noun_components) > 1:
                    compound_nouns.append(''.join(noun_components))
                noun_components = []
    if len(noun_components) > 1:
            compound_nouns.append(''.join(noun_compounds))
            
for word in compound_nouns:
    print(word)
