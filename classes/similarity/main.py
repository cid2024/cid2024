from classes.similarity.encoder import encode, encode_mise, encode_gen
from classes.similarity.util import vector_similarity
from classes.common.data_entry import DataEntry
from bank.models import Problem

import os
import pickle


vectors = None


def get_vectors():
    global vectors
    if vectors is not None:
        return vectors
    
    file_path = os.path.join(os.path.dirname(__file__), "vectors.pkl.usage")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        file = open(file_path, "rb")
        vectors = pickle.load(file)
        file.close()

    if vectors is None:
        vectors = {}
    
    return vectors


def evaluate(problem, overwrite = False):
    get_vectors()
    global vectors
    if overwrite or problem.id not in vectors:
        vectors[problem.id] = encode_gen(problem)

    file_path = os.path.join(os.path.dirname(__file__), "vectors.pkl.usage")
    file = open(file_path, "wb")
    pickle.dump(vectors, file)
    file.close()


def similarity(problem_text1: str, problem_text2: str) -> float:
    return vector_similarity(encode(problem_text1), encode(problem_text2))


def similarity_mise(problem1: DataEntry, problem2: DataEntry) -> float:
    return vector_similarity(encode_mise(problem1), encode_mise(problem2))


def similarity_gen(problem1: Problem, problem2: Problem) -> float:
    evaluate(problem1)
    evaluate(problem2)
    return vector_similarity(vectors[problem1.id], vectors[problem2.id])
