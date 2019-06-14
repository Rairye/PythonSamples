#複合名詞を探すためのスクリプト
#Uses MeCab
import MeCab

tagger = MeCab.Tagger()

compound_nouns = []

fileName = ""
lines = open(fileName, encoding='utf-8')

for line in lines:
    current_line = tagger.parse(line)
    words = current_line.split("\n")
    i = 0
    noun_components = []
    while i < len(words) - 2 :
        current_word = words[i].split("\t")
        if current_word[1].startswith("名詞"):
            noun_components.append(current_word[0])
        else:
            if len(noun_components) > 1:
                compound_nouns.append(''.join(noun_components))
            noun_components = []
        i+=1

for word in compound_nouns:
    print(word)
