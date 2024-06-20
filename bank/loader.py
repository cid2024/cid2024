import pickle
import pprint
import random
from pathlib import Path

from bank import models
import bank.choose_all as bank_choose_all
import bank.map as bank_map
import bank.region as bank_region
import bank.tf as bank_tf
import bank.db_bank as bank_mise


# Get (id, problem) dictionary of all problems in 'bank/'
def get_problems_dict() -> dict[str, models.Problem]:
    problems: list[models.Problem] = []

    bank_choose_all.load_db()
    problems.extend(bank_choose_all.choose_all_problems)

    bank_map.load_db_map_problems()
    problems.extend(bank_map.map_problems)

    bank_region.load_db_region_blank_problems()
    problems.extend(bank_region.region_blank_problems)

    bank_tf.load_db()
    problems.extend(bank_tf.tf_problems)

    bank_mise.load_db()
    problems.extend(bank_mise.mise_problems)

    # for debugging
    random.shuffle(problems)
    problems = problems[:5]

    return {
        problem.id: problem
        for problem in problems
    }


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    problems_dict = get_problems_dict()

    pp.pprint(problems_dict)
    print(len(problems_dict))
