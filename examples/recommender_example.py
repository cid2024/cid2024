from classes.recommender.main import recommend_problem

import bank.models as models
from bank.loader import get_problems_dict
from pathlib import Path

import pickle
import random

if __name__ == "__main__":
    problems: list[models.Problem] = list(get_problems_dict().values())
    random.seed(777)
    sampled = random.sample(problems, 20)
    example_history = [ (sampled[3*idx], idx%2 == 1) for idx in range(7) ]
    print(recommend_problem(example_history, sampled))
    