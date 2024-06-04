from classes.similarity.encoder import encode_problem
from settings.db_loader import get_full_data

import time

if __name__ == "__main__":
    example_problem_indices = [63762, 324569, 1789, 356058, 324569, 456541, 194228, 455028]

    data = get_full_data()
    for problem_index in example_problem_indices:
        start_time = time.time()
        print(encode_problem(data["Problem"][problem_index]).shape)
        end_time = time.time()
        print(f"Elapsed time: {end_time - start_time:.4f} seconds")