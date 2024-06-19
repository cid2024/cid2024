from classes.similarity.encoder import encode, encode_mise, encode_gen
from classes.similarity.util import vector_similarity

import os
import pickle

def similarity(problem_text1, problem_text2):
    return vector_similarity(encode(problem_text1), encode(problem_text2))

def similarity_mise(problem1, problem2):
    return vector_similarity(encode_mise(problem1), encode_mise(problem2))

vectors = None

def get_vectors():
    global vectors
    if vectors is not None:
        return vectors
    
    file_path = os.path.join(os.path.dirname(__file__), "vectors.pkl")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        file = open(file_path, "rb")
        vectors = pickle.load(file)
        file.close()

    if vectors == None:
        vectors = {}
    
    return vectors

def evaluate(problem, overwrite = False):
    get_vectors()
    global vectors
    if overwrite or problem.id not in vectors:
        vectors[problem.id] = encode_gen(problem)

    file_path = os.path.join(os.path.dirname(__file__), "vectors.pkl")
    file = open(file_path, "wb")
    pickle.dump(vectors, file)
    file.close()

def similarity_gen(problem1, problem2):
    evaluate(problem1)
    evaluate(problem2)
    return vector_similarity(vectors[problem1.id], vectors[problem2.id])
