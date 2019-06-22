# Inverted index example for searching for text in document.
# Requires NLTk
# License of corpus: Creative Commons

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import state_union

text = state_union.raw("1993-Clinton.txt").split("\n")
text = [item.strip() for item in text if (len(item) > 0 and item != ' ')]
document = []

for line in text:
    sentence_splits = sent_tokenize(line)
    for sent in sentence_splits:
        document.append(sent)

stop_words = set(stopwords.words('english'))

inverted_index = {}

def normalize(line):
    line = line.lower()
    line = line.translate(str.maketrans('', '',',!?.()""'))
    return line

document_index = 0

for sentence in document:
    word_counts = {}
    sentence = normalize(sentence)
    words = word_tokenize(sentence)
    for word in words:
        if word not in stop_words:
            if not word in word_counts:
                word_counts[word] = 1
            else:
                count = word_counts[word]
                word_counts[word] = count + 1

    for key in word_counts.keys():
        if key not in inverted_index:
            value = list()
            value.append((document_index, word_counts[key]))
            inverted_index[key] = value
        else:
            counts = inverted_index[key]
            value = (document_index, word_counts[key])
            counts.append(value)
            inverted_index[key] = counts

    document_index +=1

#Searches for a series of words
    
def search_string (search_string):
    indexes1 = set()
    results = []
    norm_search_string = normalize(search_string)
    search_words = word_tokenize(norm_search_string)
    
    if len(norm_search_string) == 0:
        print ("No results.")
    else:
        non_stop_words = []

        for word in search_words:
            if not word in stop_words:
                non_stop_words.append(word)

        if len(non_stop_words) == 0:
            print("Invalid search string. Please try again.")
            return
        else:
            for word in  non_stop_words:
                indexes2 = set()
                if word not in inverted_index:
                    print("No results.")
                    return
                else:
                    index_list = inverted_index[word]
                    for value in index_list:
                        indexes2.add(value[0])
                    if len(indexes1) == 0:
                        indexes1 = indexes2
                    else:
                        result = indexes1.intersection(indexes2)
                        if len(result) == 0:
                           
                            print("No results.")
                            return
                        else:
                            indexes1 = result

        
    for num in indexes1:       
        if search_string.lower() in document[num].lower():
            result = "Line " + str(num+1) + "\n" + document[num]
            results.append(result)


    if len(results) == 0:
       print("No results.")
    else:
        print("\nResults: \n\n")
        for result in results:
             print(result + "\n\n")


def sort_by_count(number):
    return number[1]

#Searches for a single word and returns the results in order of frequency

def search_single(word):
    norm_search_word= normalize(word)
    results = []

    if len(norm_search_word.split(" ")) > 1 or len(word) == 0:
        print("Invalid search term. Please enter a single word and try again.")
        return
    if norm_search_word not in inverted_index:
        print("No results")
    else:
        indexes = inverted_index[norm_search_word]
        indexes.sort(key=sort_by_count, reverse=True)
        
        for num in indexes:
            index= num[0]
            result = "Line " + str(index+1) + "\n" + document[index]
            results.append(result)

    print("\nResults: \n\n")
    for result in results:
        print(result + "\n\n")

print("\n\nExample one\n")
search_string("the the the")
print("\nExample two\n")
search_string("in America")
print("\nExample three\n")
search_single("President")
print("\nExample four\n")
search_single("money")
print("\nExample five\n")
search_single("money money")
