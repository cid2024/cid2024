from classes.recommender.main import recommend_problem

import bank.models as models
from bank.loader import get_problems_dict
import random

if __name__ == "__main__":
    problems: list[models.Problem] = list(get_problems_dict().values())
    random.seed(777)
    sampled = random.sample(problems, 3)
    example_history = [ (sampled[0], False) ]
    print(recommend_problem(example_history, sampled))
    