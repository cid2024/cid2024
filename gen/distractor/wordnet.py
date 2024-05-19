import nltk
from nltk.corpus import wordnet as wn


nltk.download('wordnet')


def get_distractors_wordnet(syn,word):
    distractors=[]
    word= word.lower()
    orig_word = word
    if len(word.split())>0:
        word = word.replace(" ","_")
    hypernym = syn.hypernyms()
    if len(hypernym) == 0:
        return distractors
    for item in hypernym[0].hyponyms():
        name = item.lemmas()[0].name()
        if name == orig_word:
            continue
        name = name.replace("_"," ")
        name = " ".join(w.capitalize() for w in name.split())
        if name is not None and name not in distractors:
            distractors.append(name)
    return distractors


if __name__ == "__main__":
    # original_word = "lion"
    # original_word = "그리스도교"
    original_word = "Christianity"
    synset_to_use = wn.synsets(original_word,'n')[0]
    # synset_to_use = "성상숭배 문제로 크리스트교 세계가 분열되었다."
    distractors_calculated = get_distractors_wordnet(synset_to_use,original_word)
    print(original_word)
    print(synset_to_use)
    print(distractors_calculated)

    original_word = "cricket"
    syns = wn.synsets(original_word,'n')
    for syn in syns:
        print(syn, ": ",syn.definition(),"\n" )
    synset_to_use = wn.synsets(original_word,'n')[0]
    distractors_calculated = get_distractors_wordnet(synset_to_use,original_word)
    print("\noriginal word: ",original_word.capitalize())
    print(distractors_calculated)
    original_word = "cricket"
    synset_to_use = wn.synsets(original_word,'n')[1]
    distractors_calculated = get_distractors_wordnet(synset_to_use,original_word)
    print("\noriginal word: ",original_word.capitalize())
    print(distractors_calculated)

    # "서울은 대한민국의 수도이다."
    # "미국은 1776년에 영국으로부터 독립했다."
    # "성상숭배 문제로 크리스트교 세계가 분열되었다."
    # "고조선은 8조법을 만들어 사회질서를 유지하였다."
    # "서울대학교는 신림동 산56-1번지에 위치하고 있다."
