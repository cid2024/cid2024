from sense2vec import Sense2Vec
from collections import OrderedDict


#: https://github.com/explosion/sense2vec?tab=readme-ov-file#pretrained-vectors
#: cat s2v_reddit_2019_lg.tar.gz.* > s2v_reddit_2019_lg.tar.gz

s2v = Sense2Vec().from_disk('data/s2v_reddit_2019_lg')


def sense2vec_get_words(word, s2v):
    output = []
    word = word.lower()
    word = word.replace(" ", "_")

    sense = s2v.get_best_sense(word)
    most_similar = s2v.most_similar(sense, n=20)

    # print ("most_similar ",most_similar)

    for each_word in most_similar:
        append_word = each_word[0].split("|")[0].replace("_", " ").lower()
        if append_word.lower() != word:
            output.append(append_word.title())

    out = list(OrderedDict.fromkeys(output))
    return out


if __name__ == "__main__":
    # word = "Natural Language processing"
    # word = "그리스도교"
    word = "Christianity"
    distractors = sense2vec_get_words(word,s2v)

    print("Distractors for ",word, " : ")
    print(distractors)
