import os
import pickle

from classes.similarity.encoder import encode_problem
from settings.db_loader import get_full_data

vectors = None

def evaluate(indices):
    get_vectors()
    problems = get_full_data()["Problem"]
    for index in indices:
        problem = problems[index]
        vectors[index] = encode_problem(problem)

    file_path = os.path.join(os.path.dirname(__file__), "vectors.pkl")
    file = open(file_path, "wb")
    pickle.dump(vectors, file)
    file.close()

def get_vectors():
    global vectors
    if vectors is not None:
        return vectors
    
    file_path = os.path.join(os.path.dirname(__file__), "vectors.pkl")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        file = open(file_path, "rb")
        vectors = pickle.load(file)
        file.close()
    else:
        vectors = {}
    
    return vectors
