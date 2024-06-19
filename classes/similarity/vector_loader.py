import os
import pickle

from classes.similarity.encoder import encode_mise
from settings.db_loader import get_full_data


vectors = None


def evaluate(indices, overwrite=False):
    get_vectors()
    global vectors
    problems = get_full_data()["Problem"]
    for index in indices:
        if overwrite or index not in vectors:
            problem = problems[index]
            vectors[index] = encode_mise(problem)

    file_path = os.path.join(os.path.dirname(__file__), "vectors_mise.pkl")
    file = open(file_path, "wb")
    pickle.dump(vectors, file)
    file.close()


def get_vectors():
    global vectors
    if vectors is not None:
        return vectors
    
    file_path = os.path.join(os.path.dirname(__file__), "vectors_mise.pkl")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        file = open(file_path, "rb")
        vectors = pickle.load(file)
        file.close()

    if vectors is None:
        vectors = {}
    
    return vectors
