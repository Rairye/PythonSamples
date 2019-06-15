#Customer service bot using cosine similarity, etc.
#Uses sklearn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def normalize_text(line):
    line = line.lower()
    line = line.translate(str.maketrans('', '', "\"$.?1%&/'()*+,;<=>[\]^_`{|}~\n“”’\ufeff"))
    return line

tfidf_vectorizer = TfidfVectorizer()

product_vocab = set()
grammar_word_vocab = set(["where", "what", "who", "how", "when", "time", "your", "you", "can", "do", "from", "are", "our"])
general_vocab = set(grammar_word_vocab)

inventory_questions = []
general_questions = []
misc_questions_comments = {}
goodbyes = ["bye", "goodbye", "see ya", "bye bye", "later"]
running = True

inventory_questions_lines = open('InventoryQuestions.txt', encoding='utf-8')
general_questions_lines = open('GeneralQuestions.txt', encoding='utf-8')
vocab_lines = open('Vocab.txt', encoding='utf-8')
misc_questions_comments_lines = open('MiscQuestionsComments.txt', encoding='utf-8')

for line in inventory_questions_lines:
    line = normalize_text(line)
    inventory_questions.append(line)
    words = line.split(" ")

    for word in words:
        general_vocab.add(word)

for line in general_questions_lines:
    general_questions.append(line.split('\n')[0])
    line = normalize_text(line)
    words = line.split(" ")

    for word in words:
        general_vocab.add(word)

for line in vocab_lines:
    line = normalize_text(line)
    product_vocab.add(line)
    general_vocab.add(line)

for line in misc_questions_comments_lines:
    sentences = line.split("\t")
    question = sentences[0]
    answer = sentences[1]
    misc_questions_comments[question] = answer.split('\n')[0]

    question = normalize_text(question)
    words = question.split(" ")
    for word in words:
        general_vocab.add(word)
        
def get_response(text):

    normalized = normalize_text(text)

    if normalized in goodbyes:
        return "Goodbye. Have a nice day."

    vocab_deviation = 0
    words = normalized.split(" ")

    for word in words:
        if word not in general_vocab:
            vocab_deviation +=1
    if vocab_deviation >= len(words):
        return "I am afraid I don't understand."
    
    target_response = ""
    question_similarity = 0.0
    
    for key in misc_questions_comments.keys():
        
        response = misc_questions_comments[key]
        comparison = [normalized, normalize_text(key)]
        matrix = tfidf_vectorizer.fit_transform(comparison)
        sim = cosine_similarity(matrix[0], matrix[1])
        sim_num = round(sim[0][0], 2)
        
        if sim_num > question_similarity:
            question_similarity = sim_num
            target_response = response

    if question_similarity >= 0.7:
        return target_response

    inventory_question_similiarity = 0.0

    for question in inventory_questions:
        
        comparison = [normalized, normalize_text(question)]
        matrix = tfidf_vectorizer.fit_transform(comparison)
        sim = cosine_similarity(matrix[0], matrix[1])
        sim_num = round(sim[0][0], 2)
        
        if sim_num > inventory_question_similiarity:
            inventory_question_similiarity = sim_num
    if inventory_question_similiarity >= 0.6:
        target_item = None
        for value in product_vocab:
            if value in normalized:
                target_item = value
                return "Yes, we sell " + target_item + "."

        if target_item == None:
            return "I am afraid we don't. Sorry."

    target_response = ""
    question_similarity = 0.0

    for question in general_questions:
        response = question
        comparison = [normalized, normalize_text(question)]
        matrix = tfidf_vectorizer.fit_transform(comparison)
        sim = cosine_similarity(matrix[0], matrix[1])
        sim_num = round(sim[0][0], 2) 
        if sim_num > question_similarity:
            question_similarity = sim_num
            target_response = response
    
    if question_similarity > 0.2:
        return target_response
    else:
        matches = 0
        normalized_response = normalize_text(target_response)
        word_split = target_response.split(" ")
        normalized_split = normalized.split(" ")
        for word in word_split:
            if word not in grammar_word_vocab and word in normalized_split:
                matches +=1
        if matches > 0:
            return target_response
        else:
            return "I am afraid I don't understand."
    
print("How may I help you ?\n")

while running:
    user_input = input("> ")
    response = get_response(user_input)
    print(response)
    if response == "Goodbye. Have a nice day.":
        running = False
