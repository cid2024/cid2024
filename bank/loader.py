import pickle
from pathlib import Path
from bank import models

# Get (id, problem) dictionary of all problems in 'bank/'
def get_problems_dict() -> dict[str, models.Problem]:
    problems_dict: dict[str, models.Problem] = {}
    parent_dir = Path(__file__).resolve().parent

    # Iterate through all files in the directory
    for pkl_file in parent_dir.glob("*.pkl.final"):
        with open(pkl_file, "rb") as f:
            problems: list[models.Problem] = pickle.load(f)
            # Add each problem to the dictionary
            for problem in problems:
                problems_dict[problem.id] = problem
    
    return problems_dict
