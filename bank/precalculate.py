from bank.loader import get_problems_dict
from bank.models import Problem
import classes.difficulty.main as difficulty
import classes.similarity.main as similarity

if __name__ == "__main__":
    problems: list[Problem] = list(get_problems_dict().values())
    for problem in problems:
        difficulty.evaluate(problem, overwrite=True)
        similarity.evaluate(problem, overwrite=True)
