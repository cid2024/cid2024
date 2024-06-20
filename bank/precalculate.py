import pprint

from bank.loader import get_problems_dict
from bank.models import Problem
import classes.difficulty.main as difficulty
import classes.similarity.main as similarity


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    selected_ids: list[str]

    with open("selected.txt", "r") as file:
        selected_ids = list(filter(None, map(str.strip, map(str, filter(None, file.readlines())))))

    pp.pprint(selected_ids)

    problems: list[Problem] = list(get_problems_dict().values())
    problems = list(filter(lambda problem: problem.id in selected_ids, problems))

    pp.pprint(set(selected_ids) - set(map(lambda problem: problem.id, problems)))

    # pp.pprint(problems)
    print(len(problems))

    for problem in problems:
        difficulty.evaluate(problem, overwrite=False)
        similarity.evaluate(problem, overwrite=False)
