from classes.similarity.encoder import encode_problem
from classes.similarity.vector_loader import evaluate, get_vectors
from classes.similarity.util import vector_similarity
from settings.db_loader import get_full_data

import time

if __name__ == "__main__":
    example_problem_indices = [63762, 324569, 1789, 356058, 324569, 456541, 194228, 455028]
    
    evaluate(example_problem_indices)
    vectors = get_vectors()

    for index1 in example_problem_indices:
        for index2 in example_problem_indices:
            sim = vector_similarity(vectors[index1], vectors[index2])
            print(f"{sim:.3f}", end=' ')
        print()
