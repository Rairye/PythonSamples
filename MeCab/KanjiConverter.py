#Inserts readings after kanji in Japanese text. (漢字の末尾に、その漢字の読みを挿入します。)
#Uses MeCab

import MeCab

tagger = MeCab.Tagger()

katakana_hiragana_dict = {"ア":"あ", "イ":"い", "ウ" : "う", "エ" : "え", "オ": "お", "カ":"か", "キ":"き", "ク" : "く", "ケ" : "け", "コ": "こ", "ガ":"が", "ギ":"ぎ", "グ" : "ぐ", "ゲ" : "げ", "ゴ": "ご",
                           "サ":"さ", "シ":"し", "ス" : "す", "セ" : "せ", "ソ": "そ", "ザ":"ざ", "ジ":"じ", "ズ" : "ず", "ゼ" : "ぜ", "ゾ": "ぞ", "タ":"た", "チ":"ち", "ツ" : "つ", "テ" : "て", "ト": "と",
                           "ダ":"だ", "ヂ":"ぢ", "ヅ" : "づ", "デ" : "で", "ド": "ど", "ナ":"な", "二":"に", "ヌ" : "ぬ", "ネ" : "ね", "ノ": "の", "ハ":"は", "ヒ":"ひ", "フ" : "ふ", "ヘ" : "ヘ", "ホ": "ほ",
                           "バ":"ぱ", "ピ":"ぴ", "プ" : "ぷ", "ペ" : "ぺ", "ポ": "ぽ", "バ":"ば", "ビ":"び", "ブ" : "ぶ", "ベ" : "べ", "ボ": "ぼ", "マ":"ま", "ミ":"み", "ム" : "む", "メ" : "め", "モ": "も",
                           "ヤ": "や", "ユ" : "ゆ", "ヨ" : "よ",  "ャ": "ゃ", "ュ" : "ゅ", "ョ" : "ょ", "ラ" : "ら", "リ" : "り", "ル" : "る", "レ" : "れ", "ロ" : "ろ", "ワ" : "わ", "ン" : "ん", "ッ" : "っ"
                           }
skip_words = set(["です", "でし", "だ", "や"])
allow_words = set(["い", "あり", "て", "で"])

lines = ["自然言語処理は楽しくて、便利です。", "薔薇が咲いています。", "綺麗な夜空"]

print("\n\n")

def convert (input):
    conversion = ""
    for char in input:
        hiragana = katakana_hiragana_dict[char]
        conversion = conversion + hiragana

    return conversion

for line in lines:
    output = ""
    current_line = tagger.parse(line)
    words = current_line.split("\n")
    i = 0
    
    while i < len(words) - 2 :
        current_word = words[i].split("\t")
        raw_word = current_word[0]
        attributes = current_word[1].split(",")
        reading_list = attributes[-3:]
        
        if reading_list[0] == reading_list[1]:
            output = output + current_word[0]
            i = i + 1
        else:
            characters = reading_list[0]
            if characters[0] not in katakana_hiragana_dict.values():
                conversion = convert(reading_list[1])
                jodoshi_searching = True if current_word[1].startswith("動詞") or current_word[1].startswith("形容詞") else False
                compound_noun_searching = True if current_word[1].startswith("名詞") else False
                j = i + 1
                 
                while jodoshi_searching:
                    next_word = words[j].split("\t")
                    
                    if len(next_word) < 2 or (next_word[0] in skip_words and current_word[1].startswith("形容詞")):
                        break
                    if (next_word[1].startswith("助動詞") or ((next_word[1].startswith("助詞") or next_word[1].startswith("動詞")) and next_word[0] in allow_words)) or (current_word[1].startswith("形容詞") and next_word[0] == "て"):
                        i = j
                        conversion = conversion + next_word[0]
                        raw_word = raw_word + next_word[0]
                        j = j + 1
                    else:
                        jodoshi_searching = False

                while compound_noun_searching:
                    next_word = words[j].split("\t")

                    if len(next_word) < 2:
                        break
                    if next_word[1].startswith("名詞"):
                        i = j
                        attributes = next_word[1].split(",")
                        reading_list = attributes[-3:]
                        conversion = conversion + convert(reading_list[1])
                        raw_word = raw_word + next_word[0]
                        j = j + 1
                    else:
                        compound_noun_searching = False

                output = output + raw_word + "(" + conversion + ")"
                i = j
            else:
                output = output + current_word[0]
                i = i + 1
    
    print("\n"+ line + " -> " + output)

print("\n\n")
