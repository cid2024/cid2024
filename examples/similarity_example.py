from classes.similarity.main import similarity_gen
import bank.models as models
from pathlib import Path

import pickle
import random

if __name__ == "__main__":
    problems: list[models.Problem] = []

    parent_dir = Path(__file__).resolve().parent.parent
    with open(parent_dir / "bank" / "choose_all_problems.pkl.final", "rb") as f:
        problems = pickle.load(f)

    random.seed(777)
    sampled = random.sample(problems, 5)

    for i in range(len(sampled)):
        for j in range(len(sampled)):
            sim = similarity_gen(sampled[i], sampled[j])
            print(f"{sim:.3f}", end=' ')
        print()
    
