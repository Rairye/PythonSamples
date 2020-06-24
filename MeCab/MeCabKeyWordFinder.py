#キーワードを探すためのスクリプト
#Uses MeCab
import MeCab
from collections import OrderedDict

tagger = MeCab.Tagger()

lines = open(fileName, encoding='utf-8')

word_counts = {}

def update_counts(word):
    if word in word_counts:
        temp_count = word_counts[word]
        word_counts[word] = temp_count + 1
    else:
        word_counts[word] = 1

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
            if len(noun_components) >= 1:
                update_counts(''.join(noun_components))
            noun_components = []
                    
        if current_word[1].startswith("動詞") or (current_word[1].startswith("形容詞") or current_word[1].startswith("副詞")):
            word = current_word[0]
            if word in word_counts:
                update_counts(word)
                    
        i+=1
    
    if len(noun_components) >= 1:
        update_counts(''.join(noun_components))

temp = OrderedDict(sorted(word_counts.items(), key=lambda t: t[1], reverse = True))
results = temp

for key in results.keys():
    print(key, ": ", results[key])
